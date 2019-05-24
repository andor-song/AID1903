"""
    dict项目用于处理数据
"""
import pymysql
import hashlib
import time

# 编写功能类 提供给服务端使用
class Database:
    def __init__(self,
                 database="Dict",
                 host='localhost',
                 user='root',
                 password='123456',
                 port=3306,
                 charset = "utf8"):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.charset = charset
        self.connect_db() #连接数据库

    def connect_db(self):
        """
            连接数据库
        :return:
        """
        self.db =  pymysql.connect(database=self.database,
                                   host = self.host,
                                   user = self.user,
                                   password = self.password,
                                   port = self.port,
                                   charset = self.charset)

    def create_cursor(self):
        """
            创建游标
        :return:
        """
        self.cur = self.db.cursor()

    def close(self):
        """
            关闭数据库
        :return:
        """
        self.cur.close()
        self.db.close()

    def register(self,name,keyword):
        """
            处理注册
        :return:
        """
        sql = "select * from user where name = '%s';"%name
        self.cur.execute(sql)
        if self.cur.fetchone():#如果查询到结果
            return False
        # 加密处理
        hash = hashlib.md5((name+"Python").encode())
        hash.update(keyword.encode())
        sql = "insert into user (name,keyword) values (%s,%s);"
        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self,name,keyword):
        """
            处理登录
        :return:
        """
        # 加密处理
        hash = hashlib.md5((name + "Python").encode())
        hash.update(keyword.encode())
        sql = "select * from user where name = %s and  keyword = %s;"
        r=self.cur.execute(sql,[name,hash.hexdigest()])
        print(r)
        if self.cur.execute(sql,[name,hash.hexdigest()]):#如果查询到结果
            return True
        else:
            return False

    def insert_history(self,name,word):
        """
            插入历史记录
        :param name:
        :param word:
        :return:
        """
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values (%s,%s,%s);"
        try:
            self.cur.execute(sql,[name,word,tm])
            self.db.commit()
        except Exception:
            self.db.rollback()

    def query(self,word):
        """
            单词查询
        :param word:
        :return:
        """
        sql = "select mean from words where word = '%s';"%word
        self.cur.execute(sql)
        mean = self.cur.fetchone()
        if mean:
            return  mean[0]
        return

    # def history(self,name,num):
    #     """
    #         历史记录查询
    #     :param name:
    #     :param num:
    #     :return:
    #     """
    #     sql = "select * from hist where name = '%s';"%name
    #     self.cur.execute(sql)
    #     history = self.cur.fetchmany(int(num))
    #     if history:
    #         return history
    #     return

    def history(self, name):
        """
            历史记录查询
        :param name:
        :return:
        """
        sql = "select * from hist where name = '%s' order by id desc limit 10;" % name
        self.cur.execute(sql)
        history = self.cur.fetchall()
        if history:
            return history
        return