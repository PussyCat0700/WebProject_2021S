# Press the green button in the gutter to run the script.
import WebServer

if __name__ == '__main__':
    port = input('Please set up the working port for the web server:')
    if port.isdigit() and int(port) in range(0, 65535):
        webserver = WebServer.WebServer(portNumber=int(port))
    else:
        print('input invalid. Applying default port number 80.')
        webserver = WebServer.WebServer()
    print("To testify the connection, simply run Client.py or follow the given instructions given above.")
    webserver.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
