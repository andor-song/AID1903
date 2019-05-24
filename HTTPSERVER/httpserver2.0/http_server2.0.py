"""
    http server 2.0
    将网页发送给浏览器展示
    *IO并发处理
    *基本的request解析
    *使用类封装
"""
from socket import *
from select import select

class HTTPServer:
    """
    将具体http server功能封装
    """
    def __init__(self,server_addr,static_dir):
        # 添加属性
        self.__server_addr = server_addr
        self.__static_dir = static_dir
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.creat_socket()
        self.bind()

    @property
    def server_addr(self):
        return self.__server_addr

    @server_addr.setter
    def server_addr(self,value):
        self.__server_addr = value

    @property
    def static_dir(self):
        return self.__static_dir

    @static_dir.setter
    def static_dir(self,value):
        self.__static_dir = value

    def creat_socket(self):
        """
            创建套接字
        :return:
        """
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,True)

    def bind(self):
        """
            绑定地址
        :return:
        """
        self.sockfd.bind(self.__server_addr)
        self.ip = self.__server_addr[0]
        self.port = self.__server_addr[1]

    def server_forever(self):
        """
            启动服务
        :return:
        """
        self.sockfd.listen(5)
        print("Listen the port %d"%self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    conffd,addr = self.sockfd.accept()
                    print("Connect from",addr)
                    self.rlist.append(conffd)
                else:
                    # 处理浏览器请求
                    self.handle(r)
            for w in ws:
                pass

    def handle(self,conffd):
        """
            处理客户端请求
        :param conffd:
        :return:
        """
        # 接收http请求
        request = conffd.recv(4096)
        # 防止浏览器断开
        if not request:
            self.rlist.remove(conffd)
            conffd.close()
            return
        print(request.decode())
        request_line = request.splitlines()[0].decode()
        info = request_line.split(" ")[1]
        print(conffd.getpeername(),":",info)
        # info分为访问网页和其他
        if info == "/" or info[-5:] == ".html":
            self.get_html(conffd,info)
        else:
            self.get_data(conffd,info)
        self.rlist.remove(conffd)
        conffd.close()

    def get_html(self,conffd,info):
        """
            处理网页
        :param conffd:
        :param info:
        :return:
        """
        if info =="/":
            # 网页文件
            filename = self.static_dir+"/index.html"
        else:
            filename = self.static_dir+info
        try:
            file_object = open(filename,"r")
        except Exception:
            # 没有网页
            responseHeaders = "HTTP/1.1 404 Not Found\r\n"
            responseHeaders += "\r\n"
            responseBody = "<h1>Sorry,Not Found the page</h1>"
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "\r\n"
            responseBody = file_object.read()
        finally:
            response = responseHeaders + responseBody
            conffd.send(response.encode())

    def get_data(self,conffd,info):
        responseHeaders = "HTTP/1.1 200 OK\r\n"
        responseHeaders += "\r\n"
        responseBody = "<h1>Waiting httpserver 3.0</h1>"
        response = responseHeaders + responseBody
        conffd.send(response.encode())

# 如何使用HTTPServer类
if __name__ == "__main__":
    #用户自己决定：地址，内容
    server_addr = ("0.0.0.0",8888)#服务器地址
    static_dir = "./static"#网页存放位置

    httpd = HTTPServer(server_addr,static_dir)#生成实例对象
    httpd.server_forever()#启动服务