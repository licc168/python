# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from start import common
from start import redisClient
from start import mysqlCli

'''

'''
urls={



      }

ua = UserAgent()
headers = {}
headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'

proxies = {}


def start():
    browser=None
    while True:
        # 代理
        try:
            ips = redisClient.getProxyData()
            for ip, status in ips.items():
                ip = str(ip, encoding="utf-8")
                if common.isUseIp(ip):
                   urls =  ["https://cn.iac-worldwide.com/api.php/Home/Taskdetail/index/if_id/826/sharefrom/8198"]
                   for url in urls:

                    flag = redisClient.isExistsStartIP(url,ip)
                    if(flag==False):

                        try:
                            redisClient.setUseStart(url, ip)

                            options = Options()
                            options.add_argument('-headless')
                            profile = webdriver.FirefoxProfile()
                            ip_ip = ip.split(":")[0]
                            ip_port = int(ip.split(":")[1])
                            options.set_preference('network.proxy.type', 1)  # 默认值0，就是直接连接；1就是手工配置代理。
                            options.set_preference('network.proxy.http', ip_ip)
                            options.set_preference('network.proxy.http_port', ip_port)
                            options.set_preference('network.proxy.ssl', ip_ip)
                            options.set_preference('network.proxy.ssl_port', ip_port)

                            options.set_preference("network.http.use-cache", False)
                            options.set_preference("browser.cache.memory.enable", False)
                            options.set_preference("browser.cache.disk.enable", False)
                            options.set_preference("browser.sessionhistory.max_total_viewers", 3)

                            options.set_preference('permissions.default.image',2 )
                            ##禁用Flash
                            options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

                            # 火狐浏览器
                            browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
                            browser.set_page_load_timeout(20)
                            browser.get(url)

                            print(url)
                            praisebg = WebDriverWait(browser, 10).until(
                                EC.presence_of_element_located((By.ID, "praisebg")))
                            redisClient.setUseIP(ip)
                        except Exception as e:

                            print(e)
                            print("浏览url出错")
                            break
                        finally:
                            if(browser !=None):
                                browser.close()
                else:
                    redisClient.deleteProxyData(ip)
        except       Exception as e:
            print( e)
            continue


start()