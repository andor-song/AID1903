"""
    服务端
"""
from socket import *
import os, sys

# 服务器地址
HOST = "0.0.0.0"
PORT = 9000
ADDR = (HOST, PORT)

# 存储用户信息
user = {}

def do_login(sockfd, name, addr):
    """
        判断是否要客户进入聊天室
    :param sockfd:
    :param name:
    :param addr:
    :return:
    """
    if name in user or "管理员" in name:
        sockfd.sendto("该用户已存在".encode(), addr)
        return
    sockfd.sendto(b"OK", addr)
    # 通知其他人
    msg = "欢迎%s进入聊天室"%name
    for i in user:
        sockfd.sendto(msg.encode(), user[i])

    # 将用户加入
    user[name] = addr

def do_chat(sockfd, name, text):
    """
        聊天
    :param sockfd:
    :param name:
    :param text:
    :return:
    """
    msg = "%s : %s" % (name, text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])


def do_quit(sockfd, name):
    """
        退出
    :param sockfd:
    :param name:
    :return:
    """
    msg = "%s退出了聊天室" % name
    # 将用户删除
    del user[name]
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
        else:
            sockfd.sendto(b"EXIT", user[i])

def do_request(sockfd):
    """
        接收各种客户端请求
    :param sockfd:
    :return:
    """
    while True:
        data, addr = sockfd.recvfrom(1024)
        msg = data.decode().split(" ")
        # 区分请求类型
        if msg[0] == "L":
            do_login(sockfd, msg[1], addr)
        elif msg[0] == "C":
            text = " ".join(msg[2:])
            do_chat(sockfd, msg[1], text)
        elif msg[0] == "Q":
            if msg[1] not in user:
                sockfd.sendto(b"EXIT",addr)
                continue
            do_quit(sockfd, msg[1])


def main():
    """
        创建网络连接
    :return:
    """
    # 套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    # 发送管理员消息
    elif pid == 0:
        while True:
            msg = input("超级管理员消息：")
            msg = "C 超级管理员消息 " + msg
            sockfd.sendto(msg.encode(), ADDR)
    else:
        # 请求处理
        do_request(sockfd)  # 处理客户端请求


if __name__ == "__main__":
    main()
