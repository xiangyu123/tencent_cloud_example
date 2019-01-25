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
    tempList = []
    for eveKey, eveValue in dictData.items():
        tempList.append(str(eveKey) + "=" + str(eveValue))
    return "&".join(tempList)

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
    return "&".join(resultList)

secretId = "AKID8agSPCVa8C3rPLJe3CtLXU2OZVBFLpNH"
secretKey = "5whpvqjmluyqzpSu7KSHsMBTXAd8QFJJ"

timeData = str(int(time.time()))
nonceData = int(random.random()*10000) 
actionData = "DescribeInstances"
uriData = "cvm.tencentcloudapi.com"
signMethod="HmacSHA256"
requestMethod = "GET"
regionData = "ap-beijing"
versionData = '2017-03-12'

signDictData = {
    'Action' : actionData,
    'Nonce' : nonceData,
    'Region' : regionData,
    'SecretId' : secretId,
    'SignatureMethod':signMethod,
    'Timestamp' : int(timeData),
    'Version':versionData ,
}

requestStr = "%s%s%s%s%s"%(requestMethod,uriData,"/","?",signStrFun(signDictData))

signData = urllib.parse.quote(sign(secretKey,requestStr,signMethod))

actionArgs = signDictData
actionArgs["Signature"] = signData

requestUrl = "https://%s/?"%(uriData)
requestUrlWithArgs = requestUrl + dictToStr(actionArgs)

responseData = urllib.request.urlopen(requestUrlWithArgs).read().decode("utf-8")

print(responseData)
