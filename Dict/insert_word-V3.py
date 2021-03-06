import pymysql
file_object = open("dict.txt")
db = pymysql.connect(database = "Dict",
                     host = "localhost",
                     port = 3306,
                     user = "root",
                     password = "123456",
                     charset = "utf8")
cur = db.cursor()
sql ='insert into newwords (word,mean) values (%s,%s);'

for line in file_object:
    if not line:
        break
    wordline = line.split(" ")
    word = wordline[0]
    wordline.remove(wordline[0])
    ws = " ".join(wordline)
    mean = "".join(ws.strip(" "))
    try:
        cur.execute(sql,[word,mean])
        db.commit()
    except:
        db.rollback()

file_object.close()
cur.close()
db.close()


