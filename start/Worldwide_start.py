# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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


headers = { "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",

            "Cookie":"PHPSESSID=mrhmor3am99g79g60ggaopv2p5; __jsluid=f0d0aa42cc263c37f2a9b43846dd3553; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1517629529; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=151762959",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36" }


def start():
    browser=None
    while True:
        # 代理
        try:
            ips = redisClient.getProxyData()
            for ip, status in ips.items():
                ip = str(ip, encoding="utf-8")
                if common.isUseIp(ip):
                   urls =  mysqlCli.icaUrls()
                   mysqlCli.updateStatus(1,0)
                   for row in urls:
                    id = row[0]
                    url = row[1]
                    flag = redisClient.isExistsStartIP(url,ip)
                    if(flag==False):
                        try:
                            # 最大条数
                            max = row[3]
                            #最大点赞量
                            maxStart = row[4]
                            # 当前点赞条数
                            count = mysqlCli.getStartNumById(id)

                            if count ==None:
                                count=0
                            count = int(count)
                            if (count>= max):

                                continue

                           # 谷歌浏览器
                            # chromeOptions = Options()
                            #
                            # # chromeOptions.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
                            # chromeOptions.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
                            # chromeOptions.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
                            # # chromeOptions.add_argument('--headless')
                            # # chromeOptions.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
                            # chromeOptions.add_argument('--proxy-server=' + ip)
                            # # chromeOptions.add_experimental_option("prefs", prefs)
                            # # chromeOptions.add_argument(
                            # #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"')
                            #
                            # browser = webdriver.Chrome(chrome_options=chromeOptions)
                            # browser = webdriver.Chrome()
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

                            options.set_preference("network.http.use-cache", False);
                            options.set_preference("browser.cache.memory.enable", False);
                            options.set_preference("browser.cache.disk.enable", False);
                            options.set_preference("browser.sessionhistory.max_total_viewers", 3);


                            options.set_preference('permissions.default.image',2 )
                            ##禁用Flash
                            options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

                            # 火狐浏览器
                            browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
                            browser.set_page_load_timeout(10)
                            browser.get(url)
                            print(url)


                            # if(count<maxStart):
                            # praisebg =  WebDriverWait(browser, 10).until(
                            #     EC.presence_of_element_located((By.ID, "praisebg")))
                            # # # 点赞事件
                            # praisebg.click()
                            # browser.find_element_by_id("likebg").click()
                            # 显示统计数据

                            count = count+1
                            print("url :"+url+" success:"+str(count) )
                            if(count >= max):
                                mysqlCli.updateStatus(2,1)
                            redisClient.setUseStart(url,ip)
                            redisClient.setSuccessStart(url,count)
                            mysqlCli.updatestartNum(str(count),str(id))
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