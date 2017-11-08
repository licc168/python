#!/usr/bin/python
# -*- coding: UTF-8 -*-
def isElementExist(driver,element):
	flag=True
	try:
	    driver.find_element_by_xpath(element)
	    return flag
	except:
	    flag=False
	    return flag