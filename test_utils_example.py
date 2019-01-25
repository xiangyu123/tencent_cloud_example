#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from utils.TencentCommonService import TencentCommonService

cvm_instance_example = TencentCommonService(url="https://cvm.tencentcloudapi.com", service="cvm")
#r = cvm_instance_example.execute_action("DescribeInstances", {"Limit": 10, "Offset": 0})
r = cvm_instance_example.execute_action("DescribeInstances")
print(r.text)
print(json.dumps(dict(r.headers),indent=4))
