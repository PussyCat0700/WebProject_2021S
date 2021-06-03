# import socket module
import threading
from socket import *


class WebServer:
    __defaultPort = 80
    __currentConnectionNum = 0

    def __init__(self, server_IP='0.0.0.0', portNumber=__defaultPort, maxConnectionNum=6):
        self.__maxConnectionNum = maxConnectionNum
        self.__serverSocket = socket(AF_INET, SOCK_STREAM)
        self.__serverSocket.bind((server_IP, int(portNumber)))  # 将TCP欢迎套接字绑定到指定端口
        self.__serverSocket.listen(self.__maxConnectionNum)  # 最大连接数

    def run(self, byte=1024):
        while True:
            print('Server Thread ready to activate, waiting for connections.')
            connection_socket, addr = self.__serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
            thread = threading.Thread(target=self.__serve, args=(connection_socket, addr, byte))
            thread.start()
        print('Server Closed')
        serverSocket.close()

    def __serve(self, connection_socket, addr, byte=1024):
        self.__currentConnectionNum += 1
        print('Connection from %s, current connection = %d\n' % (str(addr), self.__currentConnectionNum))
        try:
            message = connection_socket.recv(byte)  # 获取客户发送的报文
            filename = message.split()[1]  # filename='/filename'
            f = open(filename[1:])
            outputdata = f.read()
            # 发送HTTP header
            header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (
                len(outputdata))
            connection_socket.send(header.encode())

            # 循环发送outputdata的每一部分
            for i in range(0, len(outputdata)):
                connection_socket.send(outputdata[i].encode())
        except IOError:
            # 文件不存在
            header = ' HTTP/1.1 404 Not Found'
            try:
                connection_socket.send(header.encode())
            except ConnectionError:
                print("客户主机未响应")
        except IndexError:
            # 用户请求有语法错误
            header = ' HTTP/1.1 400 Bad Request'
            try:
                connection_socket.send(header.encode())
            except ConnectionError:
                print("客户主机未响应")
        except ConnectionResetError:
            print("客户主机未响应")
        # Close client socket
        finally:
            connection_socket.close()
            self.__currentConnectionNum -= 1
            print('Connection closed. Current active connections = ', self.__currentConnectionNum)
