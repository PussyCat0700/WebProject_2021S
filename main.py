# Press the green button in the gutter to run the script.
import WebServer

if __name__ == '__main__':
    port = input('Identify port number of Server:')
    if port.isdigit():
        webserver = WebServer.WebServer(portNumber=port)
    else:
        print('input invalid. Applying default port number 80.')
        webserver = WebServer.WebServer()
    webserver.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
