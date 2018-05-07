import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("47.94.196.111", "root", "11111", "iac", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()




# 查询ica 浏览信息

def  icaUrls():
    sql="select id ,url,praise_num as praiseNum, max_browse_num as maxBrowseNum , max_praise_num as maxPraiseNum ,browse_num as browseNum ,user_id as userId from iac_ad where browse_num<max_browse_num and delete_flag=0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print ("查询iac信息出错")
        return None
    # 关闭数据库连接

#获取当前浏览数量
def  getBrowseNumById(id):
    sql="select browse_num as browseNum from iac_ad where delete_flag=0 and id="+str(id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]
    except:
        print ("获取当前浏览数量出错")
        return 0

#当前点赞数量
def  getPraiseNumById(id):
    sql="select praise_num as praiseNum   from iac_ad where delete_flag=0 and id="+str(id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][0]
    except:
        print ("查询iac信息出错")
        return 0


# 将待刷状态更新为进行中
def updateStatus1():
    sql = "update iac_ad set status = 1 where status= 0  and delete_flag=0"
    try:
        cursor.execute(sql)
        db.commit()

    except:
        print("更新iac状态信息出错")
        db.commit()
    # 关闭数据库连接

def updateStatusById(status,oldStatus,id):
    sql = "update iac_ad set status = "+str(status)+" where status="+str(oldStatus)+" and delete_flag=0 and id = "+str(id)
    try:
        cursor.execute(sql)
        db.commit()

    except:
        print("更新iac状态信息出错")
        db.commit()
    # 关闭数据库连接


#更新点赞数量
def updatepraiseNum(count,id):
    sql = "update iac_ad set praise_num = "+str(count)+"  where id="+str(id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("更新数量信息出错")
        db.commit()

#更新浏览数量
def updateBrowseNum(count, id):
    sql = "update iac_ad set browse_num = " + str(count) + "  where id=" + str(id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("更新数量信息出错")
        db.commit()
    # 关闭数据库连接
