import pymysql
import re
file_object = open("dict.txt")
db = pymysql.connect(database = "Dict",
                     host = "localhost",
                     port = 3306,
                     user = "root",
                     password = "123456",
                     charset = "utf8")
cur = db.cursor()
sql ='insert into words (word,mean) values (%s,%s)'

for line in file_object:
    tuple = re.findall(r'(\w+)\s+(.*)',line)[0]
    try:
        cur.execute(sql,tuple)
        db.commit()
    except:
        db.rollback()

file_object.close()
cur.close()
db.close()


