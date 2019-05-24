"""
    dict 服务端部分
    处理请求逻辑
"""
from socket import *
from multiprocessing import Process
import signal
import sys
from operation_db import *
from time import sleep

# 全局变量
HOST = "0.0.0.0"
PORT = 8000
ADDR = (HOST,PORT)

def do_register(conffd,db,data):
    """
        处理注册
    :param conffd:
    :param db:
    :param data:
    :return:
    """
    tmp = data.split(" ")
    name = tmp[1]
    keyword = tmp[2]
    if db.register(name,keyword):
        conffd.send(b"OK")
    else:
        conffd.send(b"Fail")

def do_login(conffd,db,data):
    """
        处理登录
    :param conffd:
    :param db:
    :param data:
    :return:
    """
    tmp = data.split(" ")
    name = tmp[1]
    keyword = tmp[2]
    if db.login(name,keyword):
        conffd.send(b"OK")
    else:
        conffd.send(b"Fail")

def do_quit(conffd,db):
    """
        退出
    :param conffd:
    :param db:
    :return:
    """
    conffd.send(b"OK")

def do_query(conffd,db,data):
    """
        处理查询单词
    :param conffd:
    :param db:
    :param data:
    :return:
    """
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    #插入历史记录
    db.insert_history(name,word)
    #查询单词:未查到返回None
    mean = db.query(word)
    if not mean:
        conffd.send("没有找到该单词".encode())
    else:
        msg = "%s:%s"%(word,mean)
        conffd.send(msg.encode())

def do_history(conffd,db,data):
    """
        处理查询历史记录
    :param conffd:
    :param db:
    :param data:
    :return:
    """
    # tmp = data.split(" ")
    # name = tmp[1]
    # num = tmp[2]
    # history = db.history(name,num)
    # if not history:
    #     conffd.send("没有找到该记录".encode())
    # else:
    #     msg = ""
    #     for item in history:
    #         msg += "%s:%s %s %s\r\n"%item
    #     conffd.send(msg.encode())
    tmp = data.split(" ")
    name = tmp[1]
    history = db.history(name)
    if not history:
        conffd.send("Fail".encode())
        return
    conffd.send(b"OK")
    for item in history:
        msg = "%s:%s     %-5s     %s"%item
        sleep(0.1)#防止粘包
        conffd.send(msg.encode())
    sleep(0.1)#防止粘包
    conffd.send(b"##")

def do_request(conffd,db):
    """
        处理客户端请求
    :param conffd:
    :param db:
    :return:
    """
    db.create_cursor() #生成游标
    while True:
        data = conffd.recv(1024).decode()
        print(conffd.getpeername(), ":", data)
        if not data or data[0] == "E":
            do_quit(conffd,db)
            conffd.close()
            sys.exit("客户端退出")
        elif data[0] == "R":
            do_register(conffd,db,data)
        elif data[0] == "L":
            do_login(conffd,db,data)
        elif data[0] == "Q":
            do_query(conffd,db,data)
        elif data[0] == "H":
            do_history(conffd,db,data)

def main():
    """
        网络连接
    :return:
    """
    # 创建数据库连接对象
    db = Database()

    # 创建TCP套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 等待客户端连接
    print("Listen the port 8000")
    while True:
        try:
            conffd,addr = sockfd.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            sockfd.close()
            # db.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target= do_request,args=(conffd,db))
        p.daemon = True
        p.start()

if __name__ == "__main__":
    main()