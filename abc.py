#!/usr/bin/env python
# -*- coding: utf-8 -*-

api_tables = {
    'cvm.list': {
        'url': 'https://cvm.tencentcloudapi.com',
        'action': 'DescribeInstances',
        'params': {}
    },
    'area.list': {
        'url': 'https://cvm.tencentcloudapi.com',
        'action': 'DescribeRegions',
        'params': {"Region":""}
    },
    'user.list': {
        'url': 'https://cam.api.qcloud.com',
        'action': '',
        'params': {"Region":""}
    },

}

def api_call(key, args={}):
    pass
