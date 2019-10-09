# _*_ coding: UTF-8 _*_
# 开发团队   :  未来科技
# 开发人员   :  ww
# 开发时间   :  2019-10-09 14:47
# 文件名称   :  WebServer.py
# 开发工具   :  PyCharm
import socket
from multiprocessing import Process

def handleClient(clientSocket):
    '用一个新的进程，为一个客户端进行服务'
    recvData = clientSocket.recv(2014)
    requestHeaderLines = recvData.splitlines()
    for line in requestHeaderLines:
        print(line)

    responseHeaderLines = "HTTP/1.1 200 OK\r\n"
    responseHeaderLines += "\r\n"
    responseBody = "hello world"

    response = responseHeaderLines + responseBody
    clientSocket.send(response.encode('utf-8'))
    clientSocket.close()

def main():
    '作为程序的主控制入口'
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("", 7788))
    serverSocket.listen(10)
    while True:
        clientSocket, clientAddr = serverSocket.accept()
        clientP = Process(target=handleClient, args=(clientSocket,))
        clientP.start()
        clientSocket.close()

if __name__ == '__main__':
    main()