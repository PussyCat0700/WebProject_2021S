# import socket module
import socket
import threading
from socket import *


class WebServer(threading.Thread):
    __defaultPort = 80
    __currentConnectionNum = 0

    def __init__(self, server_IP=gethostbyname(gethostname()), portNumber=__defaultPort, maxConnection=6):
        super().__init__()
        self.__serverSocket = socket(AF_INET, SOCK_STREAM)
        self.__serverSocket.bind((server_IP, int(portNumber)))  # 绑定IP和端口号
        self.__maxConnectionNum = maxConnection
        self.__serverSocket.listen(self.__maxConnectionNum)  # 最大连接数，默认为6
        print('Your Server runs at', server_IP, 'on port', portNumber)
        print('To make connection, go ahead and visit %s:%s/helloworld.html' % (server_IP, portNumber))

    def run(self, byte=1024, time_out=60.0):
        while True:
            print('Server Thread ready to activate, waiting for connections.')
            connection_socket, addr = self.__serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
            thread = threading.Thread(target=self.__serve, args=(connection_socket, addr, byte))
            thread.start()
            thread.join(time_out)  # 超时自动回收线程
        print('Server Closed')
        serverSocket.close()

    def __serve(self, connection_socket, addr, byte=1024):
        self.__currentConnectionNum += 1
        print('Connection from %s, current connection = %d\n' % (str(addr), self.__currentConnectionNum))
        # print(threading.current_thread().name)
        try:
            message = connection_socket.recv(byte)  # 获取客户发送的报文
            filename = message.split()[1]  # filename='/filename'
            with open(filename[1:], 'rb') as f:
                file_chunk = f.read()
            # 发送HTTP header
            header = ' HTTP/1.1 200 OK\nConnection: keep-alive\nContent-Type: text/html\nContent-Length: %d\n\n' % (
                len(file_chunk))
            connection_socket.send(header.encode())
            # 循环发送file_chunk的每一部分
            send_list = [file_chunk[i:i + byte] for i in range(len(file_chunk)) if i % byte == 0]
            for send_chunk in send_list:
                connection_socket.send(send_chunk)
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
