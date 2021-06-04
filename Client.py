import multiprocessing
from socket import *


def new_client(server_addr, server_port):
    client_socket = socket()
    client_socket.connect((server_addr, server_port))
    msg = 'GET /HelloWorld.html HTTP/1.1\r\n'
    client_socket.send(msg.encode())  # 发送请求
    header_data = client_socket.recv(1024)  # 接受到的http头信息
    client_socket.close()
    return header_data


if __name__ == '__main__':
    print('This client demo only receives and displays HTTP header from your server created with main.py')
    serverAddr = gethostname()
    serverPort = 80
    user_port = input("Please input port number configured for the server:")
    if user_port.isdigit() and int(user_port) in range(0, 65535):
        serverPort = int(user_port)
    else:
        print('input invalid. Applying default port number 80.')
    retArray = []
    p = multiprocessing.Pool(7)
    print('Sending HTTP GET messages to server with multi-processing...')
    for i in range(20):
        ret = p.apply_async(new_client, args=(serverAddr, serverPort))
        retArray.append(ret)
    p.close()
    p.join()
    print('Received Headers:')
    cnt = 1
    for retItem in retArray:
        print('header ', cnt, ":")
        print(retItem.get().decode())
        cnt += 1
    input('Press Any Key To Continue.')
