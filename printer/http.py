# coding=utf8
from __future__ import print_function
import random
import socket
import math
import sys
import ssl
import os

__all__ = ['SockFeed', 'HTTPCons', 'unit_change']


if sys.version_info.major == 2:

    def s2b(s):
        return s

    def b2s(s):
        return s
else:

    def s2b(s):
        return bytes(s.encode())

    def b2s(s):
        return s.decode()


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
                    title = getattr(self, 'title', '')
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
    def __init__(self, connection):
        self.socket = connection.connect
        self.status = None
        self.raw_head = b''
        self.headers = {}
        self.data = b''
        self.progressed = 0
        self.total = 0
        self.disable_progress = False
        self.chunked = False
        self.current_chunk = None
        self.title = ''

        self.file_handle = None

    def __del__(self):
        if self.file_handle:
            self.file_handle.close()

    def clean_failed_file(self):
        if self.file_handle:
            name = self.file_handle.name
            self.file_handle.close()
            os.unlink(name)

    def save_data(self, data):
        if self.file_handle:
            self.file_handle.write(data)
        else:
            self.data += data

    @bar()
    def http_response(self, file_path='', skip_body=False, chunk=4094):
        """
        通过进度条控制获取响应结果
        :param file_path: str => 下载文件位置，若文件已存在，则在前面用数字区分版本
        :param skip_body: bool => 是否跳过http实体
        :param chunk: int => 缓存块大小
        :return:
        """
        if file_path and not self.file_handle:
            file_index = 1
            path_choice = file_path
            while os.path.exists(path_choice):
                path_choice = '{}_{}'.format(file_index, file_path)
                file_index += 1

            self.file_handle = open(path_choice, 'wb')
            self.title = os.path.basename(path_choice)

        if self.status and self.progressed == self.total:
            self.total = self.progressed = 100
            return self.data

        data = self.socket.recv(chunk)

        if not data:
            self.progressed = self.total = 100
            return True
        if not self.status:
            self.raw_head += data
            if b'\r\n\r\n' in self.raw_head:  # 接收数据直到 `\r\n\r\n` 为止
                seps = self.raw_head[0: self.raw_head.index(b'\r\n\r\n')].split(b'\r\n')
                status = seps[0].split(b' ')
                self.status = {
                    'status': status,
                    'code': status[1],
                    'version': status[0]
                }
                if self.file_handle and not self.status['code'] == b'200':
                    self.clean_failed_file()
                    self.total = self.progressed = 1
                    return False
                self.headers = {
                    i.split(b":")[0]: i.split(b":")[1].strip() for i in seps[1:]
                }
                # print("\n".join(["{} => {}".format(str(k), str(self.headers[k])) for k in self.headers]))
                if skip_body:
                    self.total = self.progressed = 100
                    return True

                if b'Content-Length' in self.headers:
                    self.total = int(self.headers[b'Content-Length'])
                else:
                    self.total = 100
                    self.chunked = True

                left = self.raw_head[self.raw_head.index(b"\r\n\r\n") + 4:]

                if left:
                    if not self.chunked:
                        self.save_data(left)
                        self.progressed += len(left)
                    else:

                        self.current_chunk = {
                            'size': int(left[: left.index(b'\r\n')], 16),
                            'content': left[left.index(b'\r\n') + 2:]
                        }

                        self.progressed = random.randrange(1, 10)

        else:
            if not self.chunked:
                self.save_data(data)
                self.progressed += len(data)
            else:
                if self.current_chunk:
                    diff = self.current_chunk['size'] - len(self.current_chunk['content'])
                    if diff > 0:
                        if len(data) > diff:
                            self.current_chunk['content'] += data[0: diff]
                            self.save_data(self.current_chunk['content'])
                            if data[diff: data.index(b'\r\n')]:
                                self.current_chunk = {
                                    'size': int(data[diff: data.index(b'\r\n')], 16),
                                    'content': data[data.index(b'\r\n') + 2:]
                                }
                            else:
                                self.current_chunk = None
                        else:
                            self.current_chunk['content'] += data
                    else:
                        self.save_data(self.current_chunk['content'][: self.current_chunk['size']])
                        left = self.current_chunk['content'][self.current_chunk['size'] + 2:] + data
                        if left:
                            self.current_chunk = {
                                'size': int(left[: left.index(b'\r\n')], 16),
                                'content': left[left.index(b'\r\n') + 2:]
                            }
                        else:
                            self.current_chunk = None
                else:
                    self.current_chunk = {
                        'size': int(data[: data.index(b'\r\n')], 16),
                        'content': data[data.index(b'\r\n') + 2:]
                    }

                if self.current_chunk and self.current_chunk['size'] == 0:
                    self.progressed = 100
                else:
                    self.progressed = random.randrange(20, 80)


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
        UA = "terminal printer user"
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


