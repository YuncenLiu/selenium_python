import pymysql


conn = pymysql.connect(host='39.105.177.10',
                       port=3388,
                       user='cloud',
                       passwd='cloud',
                       database='cloud',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
print("mysql 连接成功！")

# 创建游标对象
cursor = conn.cursor()

# 插入数据的 SQL 查询
insert_query = "INSERT INTO s_paper (p_type, p_title) VALUES (%s, %s)"

# 数据值
data = ("综合题", "2024年05月系分公共基础测试卷 测试报告")

# 执行插入操作
cursor.execute(insert_query, data)

# 提交事务
conn.commit()

# 输出插入的主键 id
print("Inserted id:", cursor.lastrowid)

# 关闭游标和数据库连接
cursor.close()
conn.close()