# -*- coding:utf8 -*-

import requests
import time
import json

from laicigou import  login
from laicigou import  config



'''
获取数据接口
'''
headers = {'content-type': 'application/json'}
def queryMarketData(pageNo,pageSize,querySortType):

    try:
        data ={
            "appId": 1,
            "lastAmount":None,
            "lastRareDegree":3,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "petIds": [],
            "querySortType": querySortType,
            "tpl":"",
            "requestId":1517730660382
        }
        print(data)
        s =  requests.post("https://pet-chain.baidu.com/data/market/queryPetsOnSale",  data=json.dumps(data), headers=headers,timeout=5)
    except:
        raise BusinessException("服务器异常")
    status =  s.status_code
    if status==200:
        res = json.loads(s.content)
        msg = res["errorMsg"]
        print(msg)
        if msg == "success":
            data = res["data"]["petsOnSale"]
            return data

        else:
            raise BusinessException("接口获取错误")
    else:
        raise BusinessException("接口异常"+str(status))
def purchase(petId,request):
    try:

        data = {
            "appId":1,
            "petId":petId,
            "requestId":1517730660382,
            "tpl":""
        }

        page = request.post("https://pet-chain.baidu.com/data/txn/create", headers=headers, data=json.dumps(data), timeout=2)
        print (page.json())
    except Exception as e:
        pass

'''
AMOUNT_ASC 金额排序
RAREDEGREE_DESC  稀有度排序
'''
def main():
    request = login.login(config.username,config.password)
    while True:
        time.sleep(2)
        try:
         data =  queryMarketData(1,10,"AMOUNT_ASC")

         for item in data:
             #没猜错的话这个是等级  0-4
             rareDegree = item["rareDegree"]
             amount = float(item["amount"])
             maxAmount = config.rares[rareDegree]
             petid = item["petId"]
             print("等级： "+str(rareDegree)+"价格："+str(amount))
             if(amount<=maxAmount):
                 purchase(petid,request)
        except BusinessException as e:
            print(e.value)
            continue





#自定义异常
class BusinessException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
main()