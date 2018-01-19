# -*- coding: utf-8 -*-
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
实现功能：
   1）根据车次和座位选票  
   2）查询超时重刷
   3）自动提交订单
   
12306相关参数
座位简写----SW:商务  YD:一等座  ED:二等座 GR:高软 PR:软 DW:动卧 YW:硬卧  YZ:硬座 RZ 软座
选座位下拉值------ 3:硬卧 1：硬座 4：软卧 O：二等座 M:一等座  9商务座
'''
username = "licchuo168"
password = "11111"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
mp_url="https://kyfw.12306.cn/otn/confirmPassenger/initDc"#购票页面

#可在cookie里面找
fromStation = "%u676D%u5DDE%2CHZH"#杭州
toStation="%u4E5D%u6C5F%2CJJG"#九江
fromDates=["2018-02-14","2018-02-13"]


#维护一个座位和下拉值的对应关系
zuowei_select = {"SW":"9","YD":"M","ED":"O","PR":"4","YW":"3","YZ":"1"}


'''
备注：车次和座位 排在前面则优先级越高
'''

# 0：车次优先  1：座位号优先
type = 1

checis=["G1463","G1583"]

zuocis=["ED","YD","GR"]


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

def main():
    browser = login()
    browser.get(ticket_url)
    count = 0
    while browser.current_url == ticket_url:
        browser.add_cookie({'name': '_jc_save_fromStation', 'value': fromStation})
        browser.add_cookie({'name': '_jc_save_toStation', 'value': toStation})
        for fromDate in fromDates:
            count += 1
            browser.add_cookie({'name': '_jc_save_fromDate', 'value': fromDate})
            browser.refresh()
            print(u'开始第 %s 次查询...' % count)
            try:
                btnElm =  WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.ID, "query_ticket")))
                btnElm.click()
            except:
                continue
            # 等待加载完成 判断是否有可预订的车次
            try:
                WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn72"))
                )
            except:
                continue
            for i in browser.find_elements_by_class_name('btn72'):
                train = i.find_element_by_xpath('../..')
                cells = train.find_elements_by_tag_name('td')
                # 车次
                tnumber = train.find_element_by_class_name('train').text
                # 始发站-结束站
                fromToStation = re.sub('\n', '-', train.find_element_by_class_name('cdz').text)
                # 始发时间-结束时间
                fromToDate = re.sub('\n', '-', train.find_element_by_class_name('cds').text)

                ls = re.sub('\n', '-', train.find_element_by_class_name('ls').text)

                # 按钮元素
                btnElm = cells[12]

                # 车次信息
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

                '''
               优先级  车次>座位号
              '''
                if type == 0:
                    for checi in checis:
                        # 判断车子是否是想要的车次
                        if tnumber == checi:
                            # 判断座位是否是想要的座位
                            for zc in zuocis:
                                # 条件满足 有票
                                if checiInfo[zc] != '--':
                                    # 座位下拉值
                                    zuoweiSelect = zuowei_select[zc]
                                    # 打印车次信息
                                    showCheciInfo(tnumber, fromToStation, fromToDate, cells)
                                    # 以上条件都满足 开始购票啦
                                    currentWin = browser.current_window_handle
                                    btnElm.click()
                                    buyTicket(browser, currentWin, zuoweiSelect)

                '''
                优先级  座位号>车次
              '''
                if type == 1:
                    for zc in zuocis:
                        if checiInfo[zc] != '--':
                            # 判断车子是否是想要的车次
                            # 判断座位是否是想要的座位
                            for checi in checis:
                                # 条件满足 有票
                                if tnumber == checi:
                                    # 座位下拉值
                                    zuoweiSelect = zuowei_select[zc]
                                    # 打印车次信息
                                    showCheciInfo(tnumber, fromToStation, fromToDate, cells)
                                    # 以上条件都满足 开始购票啦
                                    currentWin = browser.current_window_handle
                                    btnElm.click()
                                    buyTicket(browser, currentWin, zuoweiSelect)









# 打印车次信息
def showCheciInfo(tnumber,fromToStation,fromToDate,cells):
    print("车次：" + tnumber + " " + fromToStation + " " + fromToDate + "商务:" + cells[1].text
        + " 一等：" + cells[2].text + " 二等：" + cells[3].text + " 高软：" + cells[4].text + " 软：" +
          cells[5].text+ " 动卧：" + cells[6].text + " 硬卧：" + cells[7].text + " 软座：" + cells[8].text + " 硬座：" + cells[9].text)



## 进入购票页面开始购票
'''
currentWin:当前窗口
zuoweiSelect：购票页面下拉值
'''
def buyTicket(browser,currentWin,zuoweiSelect):
    # 跳转到购票页面
    handles = browser.window_handles
    for i in handles:
        if currentWin == i:
            continue
        else:
            # 将driver与新的页面绑定起来
            browser = browser.switch_to_window(i)
    # 选人 TODO 这个还需要优化 根据人名字匹配 我现在默认第一个人
    WebDriverWait(browser, 6).until(EC.presence_of_element_located((By.ID, "normalPassenger_0")))
    browser.find_element_by_id("normalPassenger_0").click()
    # 选座位
    browser.find_element_by_id("seatType_1").send_keys(zuoweiSelect)
    # 一切准备就绪 提交订单
    browser.find_element_by_id("submitOrder_id").click()
    #




# 选人啦
# def selectPerson(browser):
#     for i in browser.find_element_by_xpath("browser.find_element_by_xpath()"):

if __name__ == '__main__':
    main()




