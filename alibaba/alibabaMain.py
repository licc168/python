#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import alibabaLogin

browser = alibabaLogin.login("liccwork@126.com","111111111")
request = alibabaLogin.set_sessions(browser)
json = request.get("http://szgoldtech.en.alibaba.com/event/app/contactPerson/showContactInfo.htm?encryptAccountId=IDX1-L_yFkFFeHlkum0bTB8eAlskZoHniogxv8pKh4uAR_ZOtSg5Hrc6zYvrmUSpklIZ")
print json.encoding
print json.text.encode('utf-8')

