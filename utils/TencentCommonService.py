#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path


class TencentCommonService:
    # 初始化必须的公共参数 ["url", "service", "region", "version"]
    def __init__(self, **kw):
        temp_dict = {"version":"2017-03-12", "timestamp": int(time.time())}
        self.__dict__.update(temp_dict)
        for k,v in kw.items():
            if k not in ["url", "service", "region", "version", "Token"]:
                raise Exception("arg must in ['url', 'service', 'region', 'version', 'Token']")
            setattr(self,k,v)
        config_dir =  Path(__file__).absolute().parent.parent
        config_file = Path.joinpath(config_dir,".config")
        with open(config_file,"r",encoding="utf-8") as f:
            config_vars = json.load(f)
            for k, v in config_vars.items():
                setattr(self,k,v)

    # 拼接规范请求字符串
    def gen_request_str(self, payload_params):
        self.host =  requests.utils.urlparse(self.url).netloc
        self.payload = json.dumps(payload_params)  # payload_params must be a dict type
        canonical_headers = "content-type:application/json\nhost:{}\n".format(self.host)
        canonical_uri = "/"
        canonical_querystring = ""
        self.signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(self.payload.encode("utf-8")).hexdigest()
        canonical_request = ("POST"+ "\n" +
                     canonical_uri + "\n" +
                     canonical_querystring + "\n" +
                     canonical_headers + "\n" +
                     self.signed_headers + "\n" +
                     hashed_request_payload)
        self.canonical_request = canonical_request


    # 生成待签名的字符串
    def gen_sign_str(self):
        self.algorithm = "TC3-HMAC-SHA256"
        self.date = datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%d")
        self.credential_scope = self.date + "/" + self.service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(self.canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (self.algorithm + "\n" +
                  str(self.timestamp) + "\n" +
                  self.credential_scope + "\n" +
                  hashed_canonical_request)
        self.string_to_sign = string_to_sign

    # 签名算法
    def sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    # 进行签名
    def real_sign(self):
        secret_date = self.sign(("TC3" + self.secret_key).encode("utf-8"), self.date)
        secret_service = self.sign(secret_date, self.service)
        secret_signing = self.sign(secret_service, "tc3_request")
        self.signature = hmac.new(secret_signing, self.string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # 生成authorization
    def gen_authorization(self):
        self.authorization = (self.algorithm + " " +
                 "Credential=" + self.secret_id + "/" + self.credential_scope + ", " +
                 "SignedHeaders=" + self.signed_headers + ", " +
                 "Signature=" + self.signature)

    # 设置host头
    def set_headers(self, action):
        self.headers = {
            "Authorization": self.authorization,
            "Host": self.host,
            "Content-Type": "application/json",
            "X-TC-Action": action,
            "X-TC-Timestamp": str(self.timestamp),
            "X-TC-Version": self.version,
            "X-TC-Region": self.region,
        }


    # 发送Post请求，并返回Response
    def request_post(self):
        r = requests.post(self.url, headers=self.headers, data=self.payload)
        return r

    # 合并以上步骤
    def execute_action(self, action, payload_dict={}):
        self.gen_request_str(payload_dict)
        self.gen_sign_str()
        self.real_sign()
        self.gen_authorization()
        self.set_headers(action)
        respon = self.request_post()
        return respon
