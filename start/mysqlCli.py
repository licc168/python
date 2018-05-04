import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("47.94.196.111", "root", "11111", "iac", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()




# 查询ica 浏览信息

def  icaUrls():
    sql="select id ,url,start_num as startNum, max_browse_num as maxBrowseNum , max_start_num as maxStartNum ,user_id as userId from iac_start where start_num<max_browse_num and delete_flag=0"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except:
        print ("查询iac信息出错")
        return None
    # 关闭数据库连接

#获取当前点赞数量
def  getStartNumById(id):
    sql="select id ,url,start_num as startNum, max_browse_num as maxBrowseNum , max_start_num as maxStartNum ,user_id as userId from iac_start where delete_flag=0 and id="+str(id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        return results[0][2]
    except:
        print ("查询iac信息出错")
        return 0

def updateStatus(status,oldStatus):
    sql = "update iac_start set status = "+str(status)+" where status="+str(oldStatus)+" and delete_flag=0"
    try:
        cursor.execute(sql)
        db.commit()

    except:
        print("更新iac状态信息出错")
        db.commit()
    # 关闭数据库连接



def updatestartNum(count,id):
    sql = "update iac_start set start_num = "+count+"  where id="+id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("更新数量信息出错")
        db.commit()
    # 关闭数据库连接
