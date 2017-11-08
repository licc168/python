#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pickle
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException
import common_fun
def login(username, password):
	driver = webdriver.PhantomJS()
	driver.get("https://login.alibaba.com/")
	driver.switch_to_frame(0)
	elem = driver.find_element_by_id("fm-login-id")
	elem.clear()
	
	elem.send_keys(username)
	time.sleep(1)
	elem = driver.find_element_by_id("fm-login-password")
	elem.clear()
	elem.send_keys(password)
	time.sleep(1)
	flag = common_fun.isElementExist(driver,"//div[@id='nocaptcha' and contains(@style,'display: block;')]")
	if flag:
		dragger = driver.find_element_by_id("nc_1_n1z")
		action = ActionChains(driver)
		action.click_and_hold(dragger).perform()
		for index in range(20):
			action.move_by_offset(index, 0).perform() 
		action.reset_actions()
	

	elem = driver.find_element_by_id("fm-login-submit")
	elem.click()
	return driver

def set_sessions(browser):
	time.sleep(2)
	request = requests.Session()
	headers = {
	    "User-Agent":
	        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
	        "(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
	}
	request.headers.update(headers)
	cookies = browser.get_cookies()
	for cookie in cookies:
		#print cookie['name']+":"+cookie['value']
		request.cookies.set(cookie['name'], cookie['value'])
	return request



