"""
    客户端
"""
from socket import *
import os,sys

# 服务器地址
HOST = "176.234.8.11"
PORT = 9000
ADDR = (HOST,PORT)

def send_msg(sockfd,name):
    """
        发送消息
    :param sockfd:
    :param name:
    :return:
    """
    while True:
        try:

            text = input("\r发言：")
        except KeyboardInterrupt:
            text = "q"
        # 退出聊天室
        if text == "q":
            msg = "Q "+name
            sockfd.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")

        msg = "C %s %s"%(name,text)
        sockfd.sendto(msg.encode(),ADDR)

def recv_msg(sockfd):
    """
        接收消息
    :param sockfd:
    :return:
    """
    while True:
        data,addr = sockfd.recvfrom(2048)
        # 服务端发送EXIT表示让客户端退出
        if data.decode() == "EXIT":
            sys.exit()
        print("\r"+data.decode()+"\n发言：",end=" ")

def main():
    """
        创建网络连接
    :return:
    """
    # 套接字
    sockfd = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入姓名：")
        msg = "L " + name
        sockfd.sendto(msg.encode(), ADDR)
        # 等待回应
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == "OK":
            print("你已进入聊天室")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error")
    elif pid == 0:
        send_msg(sockfd,name)
    else:
        recv_msg(sockfd)


if __name__ == "__main__":
    main()