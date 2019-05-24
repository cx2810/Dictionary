"""
    dict项目用于处理数据
"""
import hashlib

import pymysql


class Database:
    """
        功能类,提供给服务端使用
    """

    def __init__(self,
                 host='localhost',
                 port=3306,
                 user='root',
                 passwd='tarena',
                 database='dictionary',
                 charset='utf8'):
        """
            初始化
        :param host:
        :param port:
        :param user:
        :param passwd:
        :param database:
        :param charset:
        """
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_db()

    def connect_db(self):
        """
            连接数据库
        :return:
        """
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    def create_cur(self):
        """
            创建游标
        :return:
        """
        self.cur = self.db.cursor()

    def close(self):
        """
            关闭游标,关闭数据库
        :return:
        """
        self.cur.close()
        self.db.close()

    def register(self, name, passwd):
        sql = "select * from user where name = '%s';" % name
        self.cur.execute(sql)

        re = self.cur.fetchone()
        if re:
            return False
        passwd = self.hash_md5(name, passwd)
        sql = "insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            return False

    def login(self, name, passwd):
        passwd = self.hash_md5(name, passwd)
        sql = "select * from user where name = '%s' and passwd = '%s';" % (name, passwd)
        self.cur.execute(sql)
        re = self.cur.fetchone()
        if re:
            return True
        return False

    def do_find(self, name, word):
        sql = "select mean from words where word = '%s';" % word
        self.cur.execute(sql)
        return self.cur.fetchone()

    def insert_hist(self,name,word):
        sql = "insert into hist(name,word,time) values (%s,%s,now());"
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()

    def do_look(self, name):
        sql = "select name,word,time from hist where name = %s order by id desc limit 10"
        self.cur.execute(sql, [name])
        return self.cur.fetchall()

    def hash_md5(selef, name, passwd):
        """
            加密处理
        :param name:
        :param passwd:
        :return:
        """
        hash = hashlib.md5((name + 'cx2810').encode())
        hash.update(passwd.encode())
        return hash.hexdigest()
