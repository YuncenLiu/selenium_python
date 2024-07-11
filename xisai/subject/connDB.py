import pymysql
from . import init_sql


# 获取数据库连接驱动
def getConn():
    conn = pymysql.connect(host='39.105.177.10',
                           port=3388,
                           user='cloud',
                           passwd='cloud',
                           database='cloud',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    conn.isolation_level = None
    return conn


# 携带参数插入数据
def executeSQLParams(sql, data):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    id = cursor.lastrowid
    cursor.execute('COMMIT;')
    cursor.close()
    conn.close()
    return id


# 没有参数，直接执行
def executeSQL(sql):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    id = cursor.lastrowid
    cursor.execute('COMMIT;')
    cursor.close()
    conn.close()
    return id

# 执行查询
def querySQLParams(sql,data):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql,data)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# 执行查询
def querySQL(sql):
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# 删库、重建 初始化操作
def initDb():
    conn = getConn()
    cursor = conn.cursor()
    cursor.execute(init_sql.dropPaper)
    cursor.execute(init_sql.dropSubject)
    cursor.execute(init_sql.dropSubRefPic)
    cursor.execute(init_sql.dropSubCh)
    cursor.execute(init_sql.dropSubPic)
    cursor.execute(init_sql.dropChoose)
    cursor.execute(init_sql.dropPic)
    cursor.execute(init_sql.createPaper)
    cursor.execute(init_sql.createSubject)
    cursor.execute(init_sql.createSubRefPic)
    cursor.execute(init_sql.createSubCh)
    cursor.execute(init_sql.createSubPic)
    cursor.execute(init_sql.createChoose)
    cursor.execute(init_sql.createPic)
    cursor.execute('COMMIT;')
    cursor.close()
    conn.close()
    print('数据库初始化完成！')
    return cursor.lastrowid


if __name__ == '__main__':
    # 测试初始化数据是否可用
    # initDb()
    print('测试数据库是否连接成功')
