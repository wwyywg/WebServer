# _*_ coding: UTF-8 _*_
# 开发团队   :  未来科技
# 开发人员   :  ww
# 开发时间   :  2019-10-09 15:28
# 文件名称   :  HttpServer.py
# 开发工具   :  PyCharm
import socket
from multiprocessing import Process
import re
import random
import hashlib
import os

def handleClient(clientSocket):
    # 获取客户端数据
    recvData = clientSocket.recv(2014)
    requestHeaderLines = recvData.splitlines()
    # 答应请求的头部
    # for line in requestHeaderLines:
    #     print(line)

    if requestHeaderLines[0]:
        # 获取方法地址所在的路径
        httpRequestMethodLine = requestHeaderLines[0].decode('utf-8')
        # 获取方法名字
        httpRequestMethod = httpRequestMethodLine.split()[0]
        # 获取正文部分
        httpRequestBody = requestHeaderLines[len(requestHeaderLines)-1]
        if httpRequestBody:
            print(httpRequestBody)
        # 判断cookie是否存在
        httpRequestCookies = None
        for line in requestHeaderLines:
            if "Cookie" in line.decode('utf-8'):
                httpRequestCookies = line

    # 获取path
    getFileName = re.match("[^/]+(/[^ ]*)", httpRequestMethodLine).group(1)

    if getFileName == '/':
        responseHeaderLines = "HTTP/1.1 200 OK\r\n"
        responseHeaderLines += "Content-Type: text/html;charset=utf-8\r\n"
        responseHeaderLines += "\r\n"

        responseBody = '<h1>welcome</h1><a href="./admin">进入管理后台</a >'

        response = responseHeaderLines + responseBody
        clientSocket.send(response.encode('utf-8'))
        clientSocket.close()
    elif getFileName == "/admin":
        if httpRequestCookies:      # 存在 cookie
            cookies = httpRequestCookies.decode('utf-8').split('=')
            cookie = cookies[1]

            if os.path.exists(cookie):
                responseHeaderLines = "HTTP/1.1 200\r\n"
                responseHeaderLines += "Content-Type: text/html\r\n"
                responseHeaderLines += "\r\n"
                with open(cookie, 'r') as f:
                    dataTxt = f.read()
                    responseBody = dataTxt
                # print("文件存在")
            else:
                responseHeaderLines = "HTTP/1.1 302\r\n"
                responseHeaderLines += "Location: login\r\n"
                responseHeaderLines += "Content-Type: text/html\r\n"
                responseHeaderLines += "\r\n"
                responseBody = ""
                # print("文件不存在")

        else:                       # cookie 不存在
            responseHeaderLines = "HTTP/1.1 302\r\n"
            responseHeaderLines += "Location: login\r\n"
            responseHeaderLines += "Content-Type: text/html\r\n"
            responseHeaderLines += "\r\n"
            responseBody = ""

        response = responseHeaderLines + responseBody
        clientSocket.send(response.encode('utf-8'))
        clientSocket.close()
    elif getFileName == "/login":
        responseBody = '<form action="login" method="post">'
        responseBody += '用户名：<input type="text" name="username" placeholder="请输入用户名">'
        responseBody += '<br>'
        responseBody += '密&nbsp;&nbsp;码：<input type="password" name="password" placeholder="请输入密码">'
        responseBody += '<br>'
        responseBody += '<input type="submit" value="提交">'
        responseBody += '</form>'
        if httpRequestMethod == "GET":      # GET请求
            responseHeaderLines = "HTTP/1.1 200 OK\r\n"
            responseHeaderLines += "Content-Type: text/html;charset=utf-8\r\n"
            responseHeaderLines += "\r\n"

            response = responseHeaderLines + responseBody
            clientSocket.send(response.encode('utf-8'))
            clientSocket.close()
        elif httpRequestMethod == "POST":   # POST请求
            if httpRequestBody:
                # 获取正文
                data = httpRequestBody.decode('utf-8').split('&')
                username = data[0].split('=')[1]
                password = data[1].split('=')[1]

                if username and password:
                    if username == "admin" and password == "123456":
                        rand = random.randint(100000, 999999)
                        # 创建md5对象
                        # m = hashlib.md5()
                        # m.update(str(rand).encode('utf-8'))
                        # str_md5 = m.hexdigest()
                        with open(str(rand), 'w+') as f:
                            f.write(username)

                        # print("登录成功!!!")
                        responseHeaderLines = "HTTP/1.1 302\r\n"
                        # responseHeaderLines += "Content-Type: application/octet-stream\r\n"
                        responseHeaderLines += "Set-Cookie:SESSID=%d\r\n"%rand
                        # responseHeaderLines += "Content-Disposition:attachment;filename=%s\r\n"%str_md5
                        responseHeaderLines += "Location: admin\r\n"
                        responseHeaderLines += "\r\n"

                        responseBody = username

                        response = responseHeaderLines + responseBody
                        clientSocket.send(response.encode('utf-8'))
                        clientSocket.close()
                    else:
                        # print("用户名或密码不正确！！！")
                        responseHeaderLines = "HTTP/1.1 200\r\n"
                        responseHeaderLines += "Content-Type: text/html;charset=utf-8\r\n"
                        responseHeaderLines += "\r\n"
                        responseBody += "<font color='red'>用户名或密码不正确！！！</font>"

                        response = responseHeaderLines + responseBody
                        clientSocket.send(response.encode('utf-8'))
                        clientSocket.close()
                else:
                    # print("用户名或密码不能为空！！！")
                    responseHeaderLines = "HTTP/1.1 200\r\n"
                    responseHeaderLines += "Content-Type: text/html;charset=utf-8\r\n"
                    responseHeaderLines += "\r\n"
                    responseBody += "<font color='red'>不能为空！！！</font>"

                    response = responseHeaderLines + responseBody
                    clientSocket.send(response.encode('utf-8'))
                    clientSocket.close()
    else:
        responseHeaderLines = "HTTP/1.1 200 OK\r\n"
        responseHeaderLines += "Content-Type: text/html;charset=utf-8\r\n"
        responseHeaderLines += "\r\n"
        responseBody = "404"

        response = responseHeaderLines + responseBody
        clientSocket.send(response.encode('utf-8'))
        clientSocket.close()

def main():
    '程序的住控制入口'
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(("", 7780))
    serverSocket.listen(10)
    while True:
        clientSocket, clientAddr = serverSocket.accept()
        clientP = Process(target=handleClient, args=(clientSocket,))
        clientP.start()
        clientSocket.close()

if __name__ == '__main__':
    main()
