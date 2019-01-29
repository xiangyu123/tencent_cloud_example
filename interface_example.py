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
        'method': 'GET',
        'service': 'cam',
        'url': 'https://cam.api.qcloud.com/v2/index.php',
        'action': 'ListUsers',
        'params_default': {'region': 'ap-beijing'}
    },
    'policy.list': {
        'method': "GET",
        'service': 'cam',
        'url': 'https://cam.api.qcloud.com/v2/index.php',
        'action': 'ListPolicies',
        'params_default': {'region': 'ap-beijing'}
    },
    'policy.listentitiesforpolicy': {
        'method': 'GET',
        'service': 'cam',
        'url': 'https://cam.api.qcloud.com/v2/index.php',
        'action': 'ListEntitiesForPolicy',
        'params_default': {'region': 'ap-beijing', 'policyId': 1}
    },
    'policy.listattacheduserpolicies': {
        'method': 'GET',
        'service': 'cam',
        'url': 'https://cam.api.qcloud.com/v2/index.php',
        'action': 'ListAttachedUserPolicies',
        'params_default': {'uin': '100009129850'}
    }
}


def api_call(key, args={}):
    interface_info = api_tables[key]
    rargs = {}
    rargs.update(interface_info["params_default"])
    rargs.update(args)
    region = rargs.pop("region") if "region" in rargs.keys() else ""
    req_method = (interface_info.pop("method") if "method" in interface_info.keys() else "POST").upper()
    cvm_instance_example = TencentCommonService(url=interface_info['url'],
                                                service=interface_info['service'],
                                                region=region,
                                                action=interface_info['action'],
                                                method=req_method)
    r = cvm_instance_example.execute_action(payload_dict=rargs)
    return r


if __name__ == "__main__":
    ## 查询北京的服务器 https://cloud.tencent.com/document/api/213/15728
    #c = api_call('cvm.list', {"region": "ap-beijing"})
    #print(c.text)


    ## 查询所有区域 https://cloud.tencent.com/document/api/213/15708
    #d = api_call('area.list', {"region": ""})
    #d = api_call('area.list')
    #j = json.loads(d.text)
    #print(json.dumps(j,indent=4, ensure_ascii=False))


    # 查询所有用户 https://cloud.tencent.com/document/api/598/15297
    h = api_call('user.list')
    k = json.loads(h.text)
    print(json.dumps(k, indent=4, ensure_ascii=False))

    # # 查询所有策略 https://cloud.tencent.com/document/api/598/15426
    # l = api_call('policy.list')
    # m = json.loads(l.text)
    # print(json.dumps(m, indent=4, ensure_ascii=False))

    # # 查询所有策略关联的实体 https://cloud.tencent.com/document/api/598/15425
    # o = api_call('policy.listentitiesforpolicy')
    # p = json.loads(o.text)
    # print(json.dumps(p, indent=4, ensure_ascii=False))

    # 查询某个指定子账号关联的所有策略 https://cloud.tencent.com/document/api/598/15423
    o = api_call('policy.listattacheduserpolicies')
    p = json.loads(o.text)
    print(json.dumps(p, indent=4, ensure_ascii=False))
