# -*- coding: utf-8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
12306 相关参数配置区域
SW:商务  YD:一等座  ED:二等座 GR:高软 PR:软 DW:动卧 YW:硬卧  YZ:硬座 RZ 软座
'''
username = "licchuo168"
password = "111111"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
mp_url="https://kyfw.12306.cn/otn/confirmPassenger/initDc"#购票页面

fromStation = "%u676D%u5DDE%2CHZH"#杭州
toStation="%u4E5D%u6C5F%2CJJG"#九江
fromDate="2018-01-19"

checi=["G1463","G1583"]

zuocis=["SW","YD","ED","GR"]


def login():
    browser = webdriver.Chrome()
    browser.get(login_url)
    time.sleep(1)
    #输入用户名
    elem = browser.find_element_by_id("username")
    elem.clear()
    elem.send_keys(username)
    #输入密码
    elem = browser.find_element_by_id("password")
    elem.clear()
    elem.send_keys(password)
    print(u"等待验证码，自行输入...")
    while True:
        if browser.current_url != initmy_url:
            time.sleep(2)

        else:

            break
    print("验证成功")
    return browser
def sp():

    browser = login()
    #browser = webdriver.Chrome()
    browser.get(ticket_url)
    browser.add_cookie({'name': '_jc_save_fromStation', 'value':fromStation})
    browser.add_cookie({'name': '_jc_save_toStation', 'value':toStation})
    browser.add_cookie({'name': '_jc_save_fromDate', 'value': fromDate})
    browser.refresh()
    time.sleep(2)
    count = 0
    while browser.current_url == ticket_url:
        count += 1
        print(u'开始第 %s 次查询...' % count)
        browser.find_element_by_link_text(u'查询').click()
        #等待加载完成 判断是否有可预订的车次
        try:
            WebDriverWait(browser, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn72"))
            )
        except:
            continue
         #遍历车次信息
        for i in browser.find_elements_by_class_name('btn72'):
            train = i.find_element_by_xpath('../..')
            cells = train.find_elements_by_tag_name('td')
            #车次
            tnumber = train.find_element_by_class_name('train').text
            #始发站-结束站
            fromToStation = re.sub('\n', '-', train.find_element_by_class_name('cdz').text)
            #始发时间-结束时间
            fromToDate= re.sub('\n', '-', train.find_element_by_class_name('cds').text)

            ls =  re.sub('\n', '-', train.find_element_by_class_name('ls').text)

            #按钮元素
            btnElm = cells[12]

            #车次信息
            checiInfo = {}
            checiInfo["SW"] = cells[1].text
            checiInfo["YD"] = cells[2].text
            checiInfo["ED"] = cells[3].text
            checiInfo["GR"] = cells[4].text
            checiInfo["PR"] = cells[5].text
            checiInfo["DW"] = cells[6].text
            checiInfo["YW"] = cells[7].text
            checiInfo["RZ"] = cells[8].text
            checiInfo["YZ"] = cells[9].text

            #判断车子是否是想要的车次
            if tnumber in checi:

                #判断座位是否是想要的座位
                zuociFlag = False
                for zc in zuocis:
                    if checiInfo[zc] != '--':
                        zuociFlag = True
                if zuociFlag :
                    print("车次：" + tnumber + " " + fromToStation + " " + fromToDate + "历时：" + fromToDate + "商务:" + cells[
                        1].text + " 一等：" + cells[2].text + " 二等：" + cells[3].text + " 高软：" + cells[4].text + " 软：" +
                          cells[5].text
                          + " 动卧：" + cells[6].text + " 硬卧：" + cells[7].text + " 软座：" + cells[8].text + " 硬座：" + cells[
                              9].text)
                    # 以上条件都满足 开始购票啦
                    btnElm.click()
                    #browser.get(mp_url)

                    browser.switch_to_window(browser.window_handles[1])
                    browser.find_element_by_id("normalPassenger_0").click() #选择联系人



sp()