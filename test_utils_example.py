#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from __future__ import print_function, absolute_import, unicode_literals

import json
from utils.TencentCommonService import TencentCommonService

cvm_instance_example = TencentCommonService(url="https://cvm.tencentcloudapi.com", service="cvm", region="ap-beijing", action="DescribeInstances")

# 以下两个都可以执行
r = cvm_instance_example.execute_action({"Limit": 10, "Offset": 0})
#r = cvm_instance_example.execute_action()
print(r.text)
print(json.dumps(dict(r.headers),indent=4))
