"""
    ftp 文件服务器-客户端
"""
from socket import *
from time import sleep
import sys

# 全局变量
HOST = "127.0.0.1"
PORT = 9999
ADDR = (HOST,PORT)

# 具体功能
class FtpClient:
    def __init__(self,sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")#发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # ok表示请求成功
        if data == "OK":
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print(data)

    def up_file(self,filename):
        try:
            file_object = open(filename, "rb")
        except Exception:
            print("文件不存在")
            return
        filename = filename.split("/")[-1]
        self.sockfd.send(("U " + filename).encode())
        while True:
            data = self.sockfd.recv(128).decode()
            if data == "OK":
                while True:
                    data = file_object.read(1024)
                    if not data:
                        sleep(0.1)
                        self.sockfd.send(b"##")
                        break
                    self.sockfd.send(data)
                file_object.close()
            else:
                print(data)
                break

    def down_file(self,filename):
        self.sockfd.send(("D "+filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            file_object = open(filename,"wb")
            while True:
                data = self.sockfd.recv(1024)
                if data == b"##":
                    break
                file_object.write(data)
            print("下载成功")
            file_object.close()
        else:
            print(data)

    def quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("谢谢使用")

# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)
    while True:
        print("------------------------------")
        print("\n-----------命令提示-----------")
        print("-------------list-------------")
        print("-----------up file------------")
        print("-----------down file----------")
        print("-------------quit-------------")
        print("------------------------------")

        cmd = input("请输入命令>>")
        if cmd.strip() == "list":
            ftp.do_list()
        elif cmd[:2] == "up":
            filename = cmd.strip().split(" ")[-1]
            ftp.up_file(filename)
        elif cmd[:4] == "down":
            filename = cmd.strip().split(" ")[-1]
            ftp.down_file(filename)
        elif cmd.strip() == "quit":
            ftp.quit()

# 网络连接
def main():
    sockfd = socket(AF_INET,SOCK_STREAM)
    try:
        sockfd.connect(ADDR)
    except Exception:
        sys.exit("连接服务器失败")
    else:
        print("""
        *******************************
        Word    Image    Video    Music
        *******************************
        """)
        cls = input("请输入文件类别>>")
        if cls not in ["Word","Image","Video","Music"]:
            print("Sorry input Error!")
            return
        else:
            sockfd.send(cls.encode())
            request(sockfd)

if __name__ == "__main__":
    main()