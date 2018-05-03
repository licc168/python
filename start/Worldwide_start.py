# -*- coding: utf-8 -*-

import requests
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Proxy
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType
from start import IPPools
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from start import common
from start import redisClient
from start import mysqlCli

'''

'''
urls={



      }


headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",

            "Cookie":"PHPSESSID=mrhmor3am99g79g60ggaopv2p5; __jsluid=f0d0aa42cc263c37f2a9b43846dd3553; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1517629529; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=151762959",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" }


def start():

    while True:
        # 代理
        try:
            ips = redisClient.getProxyData()
            for ip, status in ips.items():
                ip = str(ip, encoding="utf-8")
                if common.isUseIp(ip):
                   urls =  mysqlCli.icaUrls()
                   mysqlCli.updateStatus()
                   for row in urls:
                    id = row[0]
                    url = row[1]
                    flag = redisClient.isExistsStartIP(url,ip)
                    if(flag==False):
                        try:
                            # 最大条数
                            max = row[3]
                            # 当前点赞条数
                            count = redisClient.getSuccessStart(url)

                            if count ==None:
                                count=0
                            count = int(count)
                            if (count>= max):
                                continue
                            chromeOptions = webdriver.ChromeOptions()
                            chromeOptions.add_argument('--proxy-server=' + ip)
                            prefs = {
                               'profile.default_content_setting_values': {
                                   'images': 2
                               }
                            }
                            chromeOptions.add_experimental_option("prefs", prefs)
                            browser = webdriver.Chrome(chrome_options=chromeOptions)
                            browser.implicitly_wait(3)
                            browser.set_page_load_timeout(20)

                            browser.get(url)

                            print(url)
                            praisebg =  WebDriverWait(browser, 3).until(
                                EC.presence_of_element_located((By.ID, "praisebg")))
                            #
                            # js = "var q=document.documentElement.scrollTop=10000"
                            # browser.execute_script(js)
                            time.sleep(10)
                            # # 点赞事件
                            praisebg.click()
#
                            # 显示统计数据

                            count = count+1
                            print("url :"+url+" success"+str(count) )
                            redisClient.setUseStart(url,ip)
                            redisClient.setSuccessStart(url,count+1)
                            mysqlCli.updatestartNum(count+1,id)
                        except Exception as e:
                            print(e)
                            print("浏览url出错")
                            break
                        finally:
                            browser.close()
                else:
                    redisClient.deleteProxyData(ip)
        except  :
            print("异常")
            continue


start()