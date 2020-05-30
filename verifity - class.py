# encoding:utf-8
'''
通用文字识别（高精度版）
'''

import requests
import base64
import json
import re
import os
import pymysql
import random

class Verifity:
    ii = 0
    def __init__(self,url,request_url,data,filePath):
        self.url = url
        self.request_url = request_url
        self.data = data
        self.filePath = filePath

    def get_access(self):
        self.response = requests.post(url=self.url,data=self.data)
        print(self.response.text)
        access_token = json.loads(self.response.text)['access_token']
        return access_token

    def main_rtn(self):
        access_token = self.get_access()
        # 二进制方式打开图片文件
        filename = os.listdir(self.filePath)
        for i in filename:
            print(i)
            f = open('.\\333\\'+i, 'rb')
            img = base64.b64encode(f.read())
            params = {"image":img}
            request_url = self.request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response.json():
                print(response.json())
                words_result = response.json()['words_result']
                # print(words_result)
            self.parsing(words_result)

    def parsing(self,words_result):
            x_id = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba123456789', 20))
            x_name = '张冲冲'
            c_id = words_result[0]['words'][3:]
            c_date = [re.findall('体检日期:',words_result[3]['words']),'-'.join(re.findall('\d+',words_result[3]['words']))][1]
            c_address = words_result[5]['words'][5:]
            c_telephone = words_result[6]['words'][3:]
            c_identity = words_result[7]['words'][5:]
            s_name = words_result[8]['words'][3:]
            c_sex = words_result[9]['words'][3:]
            c_age = int(words_result[10]['words'][3:])
            c_Nation = words_result[11]['words'][3:]
            c_img = 'upload/shenfenzheng/' + c_identity + '.jpg'
            c_jkzurl = 'upload/shenfenzheng/' + c_identity + 'JKZ.jpg'
            print(x_id)
            print(x_name)
            print(c_id)
            print(c_date)
            print(c_address)
            print(c_telephone)
            print(c_identity)
            print(s_name)
            print(c_sex)
            print(c_age)
            print(c_Nation)
            print(c_img)
            print(c_jkzurl)
            # self.insert_sql(x_id,x_name,c_date,c_id,c_date,c_address,c_telephone,c_identity,s_name,c_sex,c_age,c_Nation,c_img,c_id,c_jkzurl)


    def insert_sql(self,x_id,x_name,c_date,c_id,c_address,c_telephone,c_identity,s_name,c_sex,c_age,c_Nation,c_img,c_jkzurl):
        # 打开数据库连接
        db = pymysql.connect("140.249.221.206", "zz", "DdNjYryPxZ3nMndm", "zz")

        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()

        # SQL 插入语句
        sql = """INSERT INTO jk_medical_info_copy1(id,create_name,create_date,tj_no,
                 tj_date,sfzaddress,tjtel,sfzno,tj_name,tj_sex,tj_age,tj_nation,tj_img,areacode,jkzurl)
                 VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%s","%s","%s","%s")"""%(x_id,x_name,c_date,c_id,c_date,c_address,c_telephone,c_identity,s_name,c_sex,c_age,c_Nation,c_img,c_id,c_jkzurl)
        # # 执行sql语句
        # cursor.execute(sql)
        # # 提交到数据库执行
        # db.commit()
        # print("@@@@@@")
        # ii += 1
        # print(ii)
        try:
           # 执行sql语句
            cursor.execute(sql)
           # 提交到数据库执行
            db.commit()
            print("######")
            verifity.ii += 1
            print(verifity.ii)
        except:
            print("$$$$$$")
            # 如果发生错误则回滚
            db.rollback()
            verifity.ii += 1
            print(verifity.ii)
        # 关闭数据库连接
        db.close()

url = "https://aip.baidubce.com/oauth/2.0/token"
request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
data = {
    'grant_type':'client_credentials',
    'client_id':'LXrztEOzQxfef66DLIDQYpIG',
    'client_secret':'gbDodnochc8jYjlAHADDgyyas9mrlmkF',
    }
filePath = r'.\333'
verifity = Verifity(url,request_url,data,filePath)
verifity.main_rtn()