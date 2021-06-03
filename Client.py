from socket import *


class Client:
    def __init__(self):
        pass

    def receive(self):
        serverAddr = ('192.168.238.1', 80)
        clientSocket = socket()
        clientSocket.connect(serverAddr)
        msg = 'GET /HelloWorld.html HTTP/1.1\r\n'
        clientSocket.send(msg.encode())  # 发送请求
        while True:
            data = clientSocket.recv(1024)  # 接受到的http头信息
            if data:
                print("From server:", data.decode())  # 转换为字节串
        clientSocket.close()
