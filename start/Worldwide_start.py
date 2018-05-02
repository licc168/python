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
                   for url in urls.keys():
                    flag = redisClient.isExistsStartIP(url,ip)
                    if(flag==False):
                        try:
                            # 最大条数
                            max = urls[url]
                            # 当前点赞条数
                            count = redisClient.getSuccessStart(url)
                            if count ==None:
                                count=0

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

                            browser.set_page_load_timeout(20)
                            browser.get(url)
                            # seatType_1 = WebDriverWait(browser, 2).until(
                            #     EC.presence_of_element_located((By.ID, "likebg")))
                            # 点赞事件
                            browser.find_element_by_id("likebg").click()
                            time.sleep(1)
                            # 显示统计数据
                            browserNum = browser.find_element_by_class_name("readnum").text
                            startNum = browser.find_element_by_id("praisenum").text
                            count = count+1
                            urls[url] =count
                            print("url :"+url+" "+ browserNum + "  :点赞数：" + startNum+"  成功条数："+str(count) )
                            redisClient.setUseStart(url,ip)
                            redisClient.setSuccessStart(url,count+1)
                        except :
                            break
                        finally:
                            browser.close()
                else:
                    redisClient.deleteProxyData(ip)
        except :
            continue


start()