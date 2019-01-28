#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import hashlib
import hmac
import sys
import urllib.parse
import urllib.request
import requests
import time
import random
import json

def sign(secretKey, signStr, signMethod):
    if sys.version_info[0] > 2:
        signStr = signStr.encode("utf-8")
        secretKey = secretKey.encode("utf-8")

    if signMethod == 'HmacSHA256':
        digestmod = hashlib.sha256
    elif signMethod == 'HmacSHA1':
        digestmod = hashlib.sha1

    hashed = hmac.new(secretKey, signStr, digestmod)
    base64 = binascii.b2a_base64(hashed.digest())[:-1]

    if sys.version_info[0] > 2:
        base64 = base64.decode()

    return base64

def dictToStr(dictData):
    x = '&'.join(["{}={}".format(k, v) for k, v in dictData.items()])
    return x
    #tempList = []
    #for eveKey, eveValue in dictData.items():
    #    tempList.append(str(eveKey) + "=" + str(eveValue))
    #k = "&".join(tempList)
    #print("k is", k)
    #return k

def signStrFun(dictData):
    tempList = []
    resultList = []
    tempDict = {}
    for eveKey,eveValue in dictData.items():
        tempLowerData = eveKey.lower()
        tempList.append(tempLowerData)
        tempDict[tempLowerData] = eveKey
    tempList.sort()
    for eveData in tempList:
        tempStr = str(tempDict[eveData]) + "=" + str(dictData[tempDict[eveData]])
        resultList.append(tempStr)
    j = "&".join(resultList)
    # print("j is", j)
    return j

secretId = "AKID8agSPCVa8C3rPLJe3CtLXU2OZVBFLpNH"
secretKey = "5whpvqjmluyqzpSu7KSHsMBTXAd8QFJJ"

timeData = str(int(time.time()))
nonceData = int(random.random()*10000) 
actionData = "ListUsers"
uriData = "cam.api.qcloud.com"
signMethod="HmacSHA256"
requestMethod = "GET"
regionData = "ap-beijing"

signDictData = {
    'Action' : actionData,
    'Nonce' : nonceData,
    'Region' : regionData,
    'SecretId' : secretId,
    'SignatureMethod':signMethod,
    'Timestamp': int(timeData),
}

requestStr = "%s%s%s%s%s"%(requestMethod,uriData,"/v2/index.php","?",signStrFun(signDictData))
print('requestStr is ', requestStr)

signData = urllib.parse.quote(sign(secretKey,requestStr,signMethod))

actionArgs = signDictData
actionArgs["Signature"] = signData

requestUrl = "https://%s/v2/index.php?"%(uriData)
print(requestUrl)
requestUrlWithArgs = requestUrl + dictToStr(actionArgs)
print(requestUrlWithArgs)

responseData = urllib.request.urlopen(requestUrlWithArgs).read().decode("utf-8")
c = json.loads(responseData)

print(json.dumps(c,indent=4))
