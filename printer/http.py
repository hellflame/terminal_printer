# coding=utf8
from __future__ import print_function
import socket
import math
import time
import sys
import ssl
import os

__all__ = ['SockFeed', 'HTTPCons', 'unit_change']


if sys.version_info.major == 2:
    from cStringIO import StringIO

    def s2b(s):
        return s

    def b2s(s):
        return s
else:
    from io import StringIO

    def s2b(s):
        if isinstance(s, bytes):
            return s
        return bytes(s.encode())

    def b2s(s):
        if isinstance(s, str):
            return s
        return s.decode(errors='ignore')


def bar(width=0, fill='#'):
    """
    进度条处理
    :param width: 手动设置进度条宽度
    :param fill: 进度填充字符
    """
    def function_wrapper(func):
        def arguments(self, *args, **kwargs):
            if not hasattr(self, 'progressed') or not hasattr(self, 'total'):
                print("progressed, total attribute is needed!")
                return
            while self.progressed <= self.total:
                func(self, *args, **kwargs)
                if not hasattr(self, 'disable_progress') or not self.disable_progress:
                    if self.total <= 0:
                        print("Total Length Invalid !")
                        self.progressed = self.total = 1
                        break
                    if not width:
                        try:
                            w = int(os.popen("stty size 2>/dev/null").read().split(" ")[1])
                        except:
                            w = 50
                    else:
                        w = width
                    percent = self.progressed / float(self.total)
                    # marks count
                    percent_show = "{}%".format(int(percent * 100))
                    # marks width
                    if hasattr(self, 'title'):
                        title = os.path.basename(self.title)
                    else:
                        title = ''
                    mark_width = w - len(percent_show) - 5 - len(title) - 2
                    mark_count = int(math.floor(mark_width * percent))
                    sys.stdout.write(
                        ' ' + title + ' ' +
                        '[' + fill * mark_count + ' ' * (mark_width - mark_count) + ']  ' + percent_show + '\r')
                    sys.stdout.flush()
                    if self.progressed == self.total:
                        sys.stdout.write(" " * w + '\r')
                        sys.stdout.flush()
                        break
                else:
                    if self.progressed == self.total:
                        break
        return arguments
    return function_wrapper


class SockFeed(object):
    """
    连接响应
    """
    def __init__(self, httpConnection, chuck=1024):
        self.socket = httpConnection.connect
        self.buffer = None
        self.chuck_size = chuck
        self.head = None
        self.header = {}
        self.http_code = 0
        self.data = ''
        self.progressed = 0
        self.total = 0
        self.disable_progress = False
        self.last_stamp = time.time()
        self.top_speed = 0
        self.chucked = False
        self.title = ''

        self.file_handle = None

    def __del__(self):
        if self.file_handle:
            self.file_handle.close()

    @bar()
    def http_response(self, file_path='', skip_body=False):
        """
        通过进度条控制获取响应结果
        :param file_path: str => 下载文件位置，若文件已存在，则在后面用数字区分版本
        :param skip_body: bool => 是否跳过http实体
        :return:
        """
        if file_path and not self.file_handle:
            file_index = 1
            path_choice = file_path
            while os.path.exists(path_choice):
                path_choice = '{}.{}'.format(file_path, file_index)
                file_index += 1

            self.file_handle = open(path_choice, 'wb')
            self.title = path_choice
        if self.head and self.progressed == self.total:
            self.total = self.progressed = 100
            return self.data
        data = self.socket.recv(self.chuck_size)
        temp = StringIO(b2s(data))
        if not data:
            self.progressed = self.total = 100
            return self.data

        if not self.head or not self.header:
            self.head = temp.readline().strip()
            self.http_code = int(self.head.split(" ")[1])
            if not self.http_code == 200:
                self.total = self.progressed = 1
                if self.file_handle:
                    current_file_name = self.file_handle.name
                    self.file_handle.close()
                    os.remove(current_file_name)
                return False
            while True:
                partial = temp.readline()
                if not partial or partial == '\r\n':
                    if self.header.get("Content-Length"):
                        self.total = int(self.header.get("Content-Length"))
                    elif self.header.get("Transfer-Encoding") == 'chunked':
                        self.chucked = True
                        self.progressed = self.total = 1
                        raise Exception("chucked encoding not supported!")
                    break
                index = partial.index(":")
                key = partial[0: index].strip()
                val = partial[index + 1:].strip()
                self.header[key] = val
            if skip_body:
                self.total = self.progressed = 100
                return self.header
            left = temp.read()

            if left:
                if self.file_handle:
                    self.file_handle.write(s2b(left))
                else:
                    self.data += b2s(left)

                self.progressed += len(s2b(left))

        else:
            if self.file_handle:
                self.file_handle.write(s2b(data))
            else:
                self.data += b2s(data)
            self.progressed += len(s2b(data))


class HTTPCons(object):
    """
    启动连接，发出请求
    """
    def __init__(self, debug=False):
        self.host = ''
        self.port = 0
        self.is_debug = debug
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect = None

    def https_init(self, host, port):
        """
        https连接
        :param host: str
        :param port: int
        :return: None
        """
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_default_certs()
        self.connect = context.wrap_socket(self.s, server_hostname=host)
        # self.connect.settimeout(65)
        self.connect.connect((host, port))
        self.host = host
        self.port = port

    def http_init(self, host, port):
        """
        http连接
        :param host: str
        :param port: int
        :return: None
        """
        self.connect = self.s
        # self.connect.settimeout(60)
        self.connect.connect((host, port))
        self.host = host
        self.port = port

    def request(self, url, method='GET', headers=None, data=None):
        """
        链接解析，完成请求
        :param url: str
        :param method: str => GET | POST
        :param headers: dict
        :param data: str => post data entity
        :return: None
        """
        if '//' not in url:
            raise URLNotComplete(url, 'url protocol')
        index = url.index('//')
        ishttps = url[0: index - 1].lower() == 'https'
        host_url = url[index + 2:]
        if "/" not in host_url:
            host_url += '/'
        index = host_url.index("/")
        host_port = host_url[0: index]
        url = host_url[index:]
        port = None
        if ':' in host_port:
            split = host_port.split(":")
            host = split[0]
            port = int(split[1].split("/")[0])
        else:
            host = host_port

        if ishttps:
            if not port:
                port = 443
            self.https_init(host, port)
        else:
            if not port:
                port = 80
            self.http_init(host, port)
        self.__send(url, method, headers, post_data=data)

    def __send(self, href, method='GET', headers=None, post_data=None):
        data = """{method} {href} HTTP/1.1\r\n{headers}\r\n\r\n"""
        # UA = "{user}_on_{platform}_HELLFLAME"  # 出于隐私考虑，暂时还是不用这样的UA了
        UA = "Secret"
        if not headers:
            head = """Host: {}\r\n""".format(self.host)
            head += "User-Agent: " + UA
        else:
            head = "\r\n".join(["{}: {}".format(x, headers[x]) for x in headers])
            if 'Host' not in headers:
                head += """\r\nHost: {}""".format(self.host)
            if 'User-Agent' not in headers:
                head += "\r\nUser-Agent: " + UA
        if method == 'POST':
            if data and type(data) == str:
                # upload for one time
                head += "\r\nContent-Length: {}".format(len(post_data))
                head += "\r\n\r\n{}\r\n".format(post_data)
            else:
                raise URLNotComplete(href, 'POST data')
        elif method == 'GET':
            if post_data:
                if not type(post_data) == dict:
                    raise Exception("post data must be a dict")
                if '?' not in href[-1]:
                    href += '?'

                for i in post_data:
                    href += '{}={}&'.format(i, post_data[i])
        data = data.format(method=method, href=href, headers=head)
        if self.is_debug:
            print("\033[01;33mRequest:\033[00m\033[01;31m(DANGER)\033[00m")
            print(data.__repr__().strip("'"))
        self.connect.sendall(s2b(data))

    def __del__(self):
        if self.connect is self.s:
            self.connect.close()
        else:
            self.connect.close()
            self.s.close()


def unit_change(target):
    """
    单位换算
    :param target: unsigned int
    :return: str
    """
    if target < 0:
        return str(target)
    unit_list = ('B', 'KB', 'MB', 'GB', 'TB')
    index = 0
    target = float(target)
    while target > 1024:
        index += 1
        target /= 1024
    return "{} {}".format(round(target, 2), unit_list[index])


class URLNotComplete(Exception):
    def __init__(self, url, lack):
        self.url = url
        self.lack = lack

    def __str__(self):
        return "URL: {} missing {}".format(self.url, self.lack)
