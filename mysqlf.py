#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import config
# 打开数据库连接
def getDb():
	db = MySQLdb.connect(config.url,config.username,config.password,config.dbname )
	return db;


