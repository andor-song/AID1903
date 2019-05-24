"""
    dict客户端
    发起请求，展示结果
"""
from socket import *
from getpass import getpass
import sys

HOST = "127.0.0.1"
PORT = 8000
ADDR = (HOST,PORT)
# 全局变量(所有函数都用到sockfd)
sockfd = socket()
sockfd.connect(ADDR)

def do_register():
    """
        注册
    :return:
    """
    while True:
        name = input("User>>")
        keyword = getpass("keyword>>")
        keyword1 = getpass("Again keyword>>")
        if (' 'in name) or (' ' in keyword):
            print("用户名和密码不能有空格")
            continue
        if keyword != keyword1:
            print("两次密码不一致")
            continue
        msg = "R %s %s"%(name,keyword)
        # 发送请求
        sockfd.send(msg.encode())
        # 接收反馈
        data = sockfd.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        break

def do_login():
    """
        处理登录
    :return:
    """
    name = input("User>>")
    keyword = getpass("keyword>>")
    msg = "L %s %s"%(name,keyword)
    sockfd.send(msg.encode())
    # 等待反馈
    data = sockfd.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")

def do_query(name):
    """
        查询单词
    :param name:
    :return:
    """
    while True:
        word = input("word>>")
        if word == "##":#结束单词查询
            break
        msg = "Q %s %s"%(name,word)
        sockfd.send(msg.encode())
        # 等待回复
        data = sockfd.recv(2048).decode()
        print(data)

def do_history(name):
    """
        查询历史记录
    :param name:
    :return:
    """
    # num = input("num>>")
    # msg = "H %s %s" % (name, num)
    # sockfd.send(msg.encode())
    # # 等待回复
    # data = sockfd.recv(4096).decode()
    # print(data)
    msg = "H %s" % name
    sockfd.send(msg.encode())
    data = sockfd.recv(128).decode()
    if data == "OK":
        while True:
            data = sockfd.recv(1024).decode()
            if data =="##":
                break
            print(data)
    else:
        print("还没有历史记录")


def login(name):
    """
        二级界面
    :return:
    """
    while True:
        print("""
        ==============Query===========
         1.查单词    2.历史记录   3.注销
        ==============================
        """)
        cmd = input("请输入选项>>")
        if cmd == "1":
            do_query(name)
        elif cmd == "2":
            do_history(name)
        elif cmd == "3":
            return
        else:
            print("请输入正确命令！")

def do_quit():
    msg = "E"
    sockfd.send(msg.encode())
    # 等待反馈
    data = sockfd.recv(128).decode()
    print(data)
    if data == "OK":
        sys.exit("服务器退出")

def main():
    """
        创建网络连接
    :return:
    """
    while True:
        print("""
        ============Welcome===========
         1.注册      2.登录      3.退出
        ==============================
        """)
        try:
            cmd = input("请输入选项>>")
            if cmd == "1":
                do_register()
            elif cmd == "2":
                do_login()
            elif cmd == "3":
                do_quit()
            else:
                print("请输入正确命令！")
        except KeyboardInterrupt:
            sys.exit("客户端退出")

if __name__ == "__main__":
    main()