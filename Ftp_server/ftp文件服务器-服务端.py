"""
    ftp 文件服务器-服务端
    并发网络功能训练
"""
from socket import *
from threading import Thread
from time import sleep
import sys,os


# 全局变量
HOST = "0.0.0.0"
PORT = 9999
ADDR = (HOST,PORT)
FTP = "/home/tarena/FTP/"#文件库路径

# 将客户端请求功能封装为类
class FtpServer:
    def __init__(self, conffd,FTP_PATH):
        self.conffd = conffd
        self.FTP_PATH = FTP_PATH

    def do_list(self):
        # 获取文件列表
        files = os.listdir(self.FTP_PATH)
        if not files:
            self.conffd.send("该文件类别为空".encode())
            return
        else:
            self.conffd.send(b"OK")
            sleep(0.1)
        filelist = ""
        for file in files:
            if file[0] != "." and os.path.isfile(self.FTP_PATH+file):#判断是否为隐藏文件或者是否为普通文件
                filelist += file + "\n"  #人为添加边界
        self.conffd.send(filelist.encode())

    def up_list(self,filename):
        if os.path.exists(self.FTP_PATH + filename):
            self.conffd.send("该文件已存在".encode())
            return
        self.conffd.send(b"OK")
        file_object = open(self.FTP_PATH+filename,"wb")
        # 接收文件
        while True:
            data = self.conffd.recv(1024)
            if data == b"##":
                break
            file_object.write(data)
        file_object.close()
        self.conffd.send("上传成功".encode())

    def down_list(self,filename):
        try:
            file_object = open(self.FTP_PATH+filename,"rb")
        except Exception:
            self.conffd.send("该文件不存在".encode())
            return
        else:
            self.conffd.send(b"OK")
            sleep(0.1)
        # 发送文件内容
        while True:
            data = file_object.read(1024)
            if not data:
                sleep(0.1)
                self.conffd.send(b"##")
                break
            self.conffd.send(data)
        file_object.close()

# 客户端请求处理函数
def handle(conffd):
    # 选择文件夹
    cls = conffd.recv(1024).decode()
    FTP_PATH = FTP + cls + "/"
    ftp = FtpServer(conffd,FTP_PATH)
    while True:
        # 接收客户端请求
        data = conffd.recv(1024).decode()
        # 如果客户端断开返回data为空
        if not data or data[0] == "Q":
            return
        elif data[0] == "L":
            ftp.do_list()
        elif data[0] == "U":
            filename = data.split(" ")[-1]
            ftp.up_list(filename)
        elif data[0] == "D":
            filename = data.split(" ")[-1]
            ftp.down_list(filename)

# 网络搭建
def main():
    sockfd = socket(AF_INET,SOL_SOCKET)
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    print("Listen the port 9999...")
    while True:
        try:
            conffd,addr = sockfd.accept()
        except KeyboardInterrupt:
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        print("连接的客户端：",addr)
        # 创建线程处理请求
        client = Thread(target=handle,args=(conffd,))
        client.setDaemon(True)  # 分支线程随主线程退出
        client.start()


if __name__ == "__main__":
    main()
