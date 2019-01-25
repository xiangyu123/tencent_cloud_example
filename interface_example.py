#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from utils.TencentCommonService import TencentCommonService

api_tables = {
    'cvm.list': {
        'service': "cvm",
        'url': 'https://cvm.tencentcloudapi.com',
        'action': 'DescribeInstances',
        'params_default': {}
    },
    'area.list': {
        'service': "cvm",
        'url': 'https://cvm.tencentcloudapi.com',
        'action': 'DescribeRegions',
        'params_default': {}
    },
    'user.list': {
        'service': "cam",
        'url': 'https://cam.api.qcloud.com',
        'action': 'ListUsers',
        'params_default': {}
    },

}

args={"region":"ap-beijing"}

def api_call(key, args={}):
    interface_info = api_tables[key]
    rargs = {}
    rargs.update(interface_info["params_default"])
    rargs.update(args)
    region = rargs.pop("region") if "region" in rargs.keys() else ""
    cvm_instance_example = TencentCommonService(url=interface_info['url'], service=interface_info['service'], region=region)
    r = cvm_instance_example.execute_action(interface_info['action'], payload_dict=rargs)
    return r


if __name__ == "__main__":
#    # 查询北京的服务器
#    c = api_call('cvm.list', {"region": "ap-beijing"})
#    print(c.text)
#
#
#    # 查询所有区域
#    #d = api_call('area.list', {"region": ""})
#    d = api_call('area.list')
#    j = json.loads(d.text)
#    print(json.dumps(j,indent=4, ensure_ascii=False))


    # 查询所有用户
    h = api_call('user.list')
    print(h.text)
    #k = json.loads(h.text)
    #print(json.dumps(k,indent=4, ensure_ascii=False))
