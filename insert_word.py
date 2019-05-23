"""
    将dict.txt内容存入数据库
"""
import re

import pymysql

db = pymysql.connect(host='localhost',
                     user='root',
                     passwd='tarena',
                     database='dictionary',
                     charset='utf8')
cur = db.cursor()
sql = "insert into words(word,mean) values (%s,%s)"
with open('dict.txt', 'r') as fd:
    for line in fd:
        if not line:
            break
        # 获取匹配内容元组(word,mean)
        tup = re.findall(r'(\w+)\s+(.*)', line)[0]
        try:
            cur.execute(sql, tup)

        except Exception as e:
            print(e)
            db.rollback()
            break
db.commit()
cur.close()
db.close()
