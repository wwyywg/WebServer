### http协议内容

请求报文									响应报文

POST/GET URI 版本协议 HTTP1.1			协议版本HTTP/1.1	200		OK

header									header

Content-Type							Content-Type

Accept									Accept

...										...

空行									空行

query-String								html、json、xml、txt...

### 网络协议

网络协议分为：网络接口层(链路层)、网际层(网络层)、传输层、应用层

### HTTP 通信协议的组成

http协议是基于应用层的协议，并且在传输层使用的TCP的可靠性同性协议。

`协议是两个需要通过网络通信的程序达成的一种约定，它规定了报文的交换方式和包含的意义`

### 请求 URI 定位资源

URL（Uniform Resource Locator）,统一资源定位符，用于描述一个网络上的资源

`URI用于字符串标识某一互联网资源，而 URL 表示资源的地点（互联网上所处的位置）。可见 URL是URI的子集。`

http://www.wwyywg.com:80/python/index.html?name=mic#head
schema://host[:port#]/path/.../?[url-params]#[ query-string]

| schema       | 指定应用层使用的协议（例如：http，https，tfp） |
| ------------ | ---------------------------------------------- |
| host         | HTTP 服务器的IP地址或域名                      |
| port#        | HTTP服务器的端口                               |
| path         | 访问资源的路径                                 |
| query-string | 查询标识符                                     |

### MIME Type

是描述消息内容类型的因特网标准，常见的几种类型

文本文件：text/html,text/plain,text/css,application/xhtml+xml,application/xml

图片文件：image/jpeg,image/gif,image/png

视频文件：video/mpeg,video/quickime

可以通过两种方法来设置文件的渲染类型，第一种是 Accept，第二种是 Content-Type

> `Accept`:表示客户端希望接收的数据类型，即告诉服务器我需要什么媒体类型的数据，此时服务器应该根据Accpt 请求头生产指定媒体类型的数据
>
> `Content-Type`:表示发送端的发送的实体数据类型 application/json;charset=utf-8 表示服务端返回的数据格式是json。 