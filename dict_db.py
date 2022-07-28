import pymysql
import hashlib
salt = b"*#1007#" #加密专业盐
# 加密处理函数
def encryption(passwd):
    # 对密码进行加密处理
    hash = hashlib.md5(salt)
    hash.update(passwd.encode())
    return hash.hexdigest() # 获取存储密码

class Database:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1',
                                  user="root",
                                  password='123456',
                                  charset='utf8',
                                  database='dict',
                                  port=3306)
        self.cur = self.db.cursor()

    def login(self,name,passwd):
        passwd = encryption(passwd) # 加密转换
        sql = "select * from user where name=%s and password=%s"
        self.cur.execute(sql,[name,passwd])
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False

    def register(self,name,passwd):
        sql = "select * from user where name='%s'" % name
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return False
        # 加密
        passwd = encryption(passwd)
        #插入用户
        try:
            sql = "insert into user (name,password) values(%s,%s)"
            self.cur.execute(sql,[name,passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def history(self,name):
        sql = "select name,word,time from hist where name='%s' order by time desc limit 10" %name
        self.cur.execute(sql)
        return self.cur.fetchall()

    def query(self,word):
        sql = "select mean from words where word='%s'" % word
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return result[0]

    def insert_history(self,name,word):
        try:
            sql = "insert into hist (name,word) values ('%s','%s')"%(name,word)
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.cur.close()
        self.db.close()


