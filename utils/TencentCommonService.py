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


class AliCommonService:
    def __init__(self, url):
        config_dir =  Path(__file__).absolute().parent.parent
        config_file = Path.joinpath(config_dir,".config")
        with open(config_file,"r",encoding="utf-8") as f:
            config_vars = json.load(f)
        for k, v in config_vars.items():
            setattr(self,k,v)
        self.url = url

    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])    # 使用get请求方法

        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode('utf-8').encode('utf-8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'JSON',
            'Version': '2014-05-26',
            'AccessKeyId': self.access_id,
            'SignatureVersion': '1.0',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(self.access_secret, parameters)
        parameters['Signature'] = signature

        # return parameters
        url = self.url + "/?" + urllib.urlencode(parameters)
        return url

