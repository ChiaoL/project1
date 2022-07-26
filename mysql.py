"""
mysql.py
pymysql数据库操作流程演示
"""

import pymysql

# 连接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password = '123456',
                     database = 'stu',
                     charset='utf8')

# 创建游标 (操作数据库语句,获取查询结果)
cur = db.cursor()

# juku
cur.execute("insert into class_1 \
values (6,'Levi',11,'m',98);")
cur.commit()
cur.close()
db.close()