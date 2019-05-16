# coding=utf8
import socket
import math
import sys
import ssl
import os

from subprocess import check_output
from itertools import cycle
from functools import wraps
from time import time

__all__ = ['SockFeed', 'HTTPCons', 'unit_change', 'bar']


def bar(width=0, fill='#'):
    """
    进度条处理
    :param width: 手动设置进度条宽度
    :param fill: 进度填充字符
    """
    def function_wrapper(func):
        @wraps(func)
        def arguments(self, *args, **kwargs):
            if not hasattr(self, 'progressed') or not hasattr(self, 'total'):
                print("progressed, total attribute is needed!")
                return
            progress_cursor = 1
            last_update = 0
            while self.progressed <= self.total:
                func(self, *args, **kwargs)
                if not hasattr(self, 'disable_progress') or not self.disable_progress:
                    if self.total <= 0:
                        print("Total Length Invalid !")
                        self.progressed = self.total = 1
                        break
                    if time() - last_update > .1:
                        if not width:
                            try:
                                w = int(check_output("stty size", stderr=None, shell=True).split(b" ")[1])
                            except:
                                w = 50
                        else:
                            w = width
                        if not hasattr(self, 'chunked') or not self.chunked:
                            # 普通编码进度条
                            percent = self.progressed / float(self.total)
                            # marks count
                            percent_show = "{}%".format(int(percent * 100))
                            # marks width
                            title = getattr(self, 'title', '')
                            mark_width = w - len(percent_show) - str_len(title) - 7
                            mark_count = int(math.floor(mark_width * percent))
                            sys.stdout.write(
                                ' ' + title + ' ' +
                                '[' + fill * mark_count + ' ' * (mark_width - mark_count) + ']  ' + percent_show + '\r')
                        else:
                            # 分块编码进度条
                            progress_cursor += 1
                            title = getattr(self, 'title', '')
                            chunk_recved = unit_change(self.chunk_recved)
                            mark_width = w - str_len(title) - len(chunk_recved) - 6
                            sys.stdout.write(" " + title + " " +
                                             "[" +
                                             "".join([i for _, i in zip(range(mark_width),
                                                                        cycle([">> ", " >>", "> >"][progress_cursor % 3]))])
                                             + "] {}\r".format(chunk_recved))

                        sys.stdout.flush()
                        last_update = time()

                    if self.progressed == self.total:
                        sys.stdout.write(" " * w + '\r')
                        break
                else:
                    if self.progressed == self.total:
                        break
        return arguments
    return function_wrapper


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
    return "{:.2f} {}".format(round(target, 2), unit_list[index])


def str_len(s):
    """
    获取占用等宽字体终端实际宽度，适用`Monaco`等其他等宽字体字体
    :param s:
    :return:
    """
    length = 0
    for i in s:
        # Chinese,Japanese,Korean character utf8 range
        # Test Font `Monaco`
        if 3105 <= ord(i) <= 65535:
            length += 2
        else:
            length += 1
    return length


class SockFeed(object):
    """
    连接响应
    """
    def __init__(self, connection):
        """
        :param connection: HttpCons
        """
        self.con = connection
        self.socket = self.con.connect
        self.status = None
        self.raw_head = b''
        self.headers = {}
        self.data = b''
        self.progressed = 0
        self.total = 0
        self.disable_progress = False
        self.chunked = False
        self.current_chunk = b''
        self.chunk_recved = 0
        self.title = ''

        self.file_handle = None

    def finish_loop(self):
        """
        让进度条走满，关闭TCP连接，关闭可能还打开的文件
        :return: None
        """
        self.progressed = self.total = 100
        self.con.close()  # 关闭tcp连接
        if self.file_handle:
            self.file_handle.close()

    def clean_failed_file(self):
        """
        下载失败后清理、删除文件
        :return:
        """
        if self.file_handle:
            name = self.file_handle.name
            self.file_handle.close()
            os.unlink(name)

    def save_data(self, data):
        """
        将每次获取的HTTP实体保存进内存或文件
        :param data:
        :return:
        """
        if self.file_handle:
            self.file_handle.write(data)
        else:
            self.data += data

    def flush_chunk(self, data):
        self.current_chunk += data

        while len(self.current_chunk) > 10240 or self.current_chunk.endswith(b'0\r\n\r\n'):  # 并不意味着所有分块结束
            # 开始解析当前chunk cache
            chunk_head = self.current_chunk[: self.current_chunk.index(b'\r\n')]
            chunk_left = self.current_chunk[self.current_chunk.index(b'\r\n') + 2:]
            chunk_size = int(chunk_head, 16)
            if chunk_size == 0:
                self.finish_loop()  # 一定要用finish_loop结束请求，否则会出现未关闭的文件 !
                return True
            if chunk_size > len(chunk_left):
                # 说明当前分块没有接收完全
                return False
            valid_data = chunk_left[: chunk_size]
            self.chunk_recved += len(valid_data)
            self.save_data(valid_data)
            self.current_chunk = chunk_left[chunk_size:]
            if self.current_chunk.startswith(b'\r\n'):
                # 如果上一个分块没有吃掉最后的 \r\n，则在这里把它剔除
                self.current_chunk = self.current_chunk[2:]

    @bar()
    def http_response(self, file_path='', skip_body=False, chunk=4096, overwrite=False):
        """
        通过进度条控制获取响应结果
        :param file_path: str => 下载文件位置，若文件已存在，则在前面用数字区分版本
        :param skip_body: bool => 是否跳过http实体
        :param chunk: int => 缓存块大小
        :param overwrite: bool => 是否覆盖重名文件
        :return:
        """
        if file_path and not self.file_handle:
            path_choice = file_path
            if os.path.exists(file_path):
                if overwrite:
                    os.remove(file_path)
                else:
                    file_index = 1
                    dirname = os.path.dirname(path_choice)
                    filename = os.path.basename(path_choice)
                    while os.path.exists(path_choice):
                        path_choice = os.path.join(dirname, '{}_{}'.format(file_index, filename))
                        file_index += 1

            self.file_handle = open(path_choice, 'wb')
            self.title = os.path.basename(path_choice)

        if self.status and self.progressed == self.total:
            self.finish_loop()
            return True

        data = self.socket.recv(chunk)

        if not data:
            self.finish_loop()
            return True
        if not self.status:
            self.raw_head += data
            if b'\r\n\r\n' in self.raw_head:  # 接收数据直到 `\r\n\r\n` 为止
                seps = self.raw_head[0: self.raw_head.index(b'\r\n\r\n')].split(b'\r\n')
                status = seps[0].split(b' ')
                self.status = {
                    'status': seps[0],
                    'code': status[1],
                    'version': status[0]
                }
                if self.file_handle and not self.status['code'] == b'200':
                    self.clean_failed_file()
                    self.finish_loop()
                    return False
                self.headers = {
                    i.split(b":")[0]: i.split(b":")[1].strip() for i in seps[1:]
                }
                # print("\n".join(["{} => {}".format(str(k), str(self.headers[k])) for k in self.headers]))
                if skip_body:
                    self.finish_loop()
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

                        self.flush_chunk(left)  # 实体部分以分块大小十六进制数字开头

        else:
            if not self.chunked:
                self.save_data(data)
                self.progressed += len(data)
                if self.progressed == self.total:
                    self.finish_loop()
            else:
                self.flush_chunk(data)


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

    def __del__(self):
        self.close()

    def close(self):
        """
        需要请求接收完成之后手动关闭
        :return: None
        """
        if self.connect is self.s:
            self.connect.close()
        else:
            self.connect.close()
            self.s.close()

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
        return self.connect

    def __send(self, href, method='GET', headers=None, post_data=None):
        data = """{method} {href} HTTP/1.1\r\n{headers}\r\n\r\n"""
        UA = "TerminalPrinter http client"
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
                head += "\r\n\r\n{}".format(post_data)
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
        if method == 'POST':
            data = data[:-4]
        if self.is_debug:
            print("\033[01;33mRequest:\033[00m\033[01;31m(DANGER)\033[00m")
            print(data.__repr__().strip("'"))
        if sys.version_info.major == 3:
            self.connect.sendall(data.encode())
        else:
            self.connect.sendall(data)


class URLNotComplete(Exception):
    def __init__(self, url, lack):
        self.url = url
        self.lack = lack

    def __str__(self):
        return "URL: {} missing {}".format(self.url, self.lack)


if __name__ == '__main__':
    import unittest
    import hashlib
    import tempfile

    class HTTPTest(unittest.TestCase):
        """
        static.hellflame.net 域名下的文件大多数情况下都是chunked编码
        raw.githubusercontent.com 域名下文件未分块
        """
        def test_https_request(self):
            req = HTTPCons()
            connect = req.request("https://static.hellflame.net/resource/de5ca9cf5320673dc43b526e3d737f05")
            self.assertEqual(req.host, 'static.hellflame.net')
            self.assertEqual(req.port, 443)
            self.assertIs(connect, req.connect)
            req.close()

        def test_http_request(self):
            req = HTTPCons()
            connect = req.request("http://static.hellflame.net/resource/de5ca9cf5320673dc43b526e3d737f05")
            self.assertEqual(req.host, 'static.hellflame.net')
            self.assertEqual(req.port, 80)
            self.assertIs(connect, req.connect)
            req.close()

        def test_response_in_memory(self):
            req = HTTPCons()
            req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")
            resp = SockFeed(req)
            resp.disable_progress = True
            resp.http_response()
            self.assertEqual(hashlib.md5(resp.data).hexdigest(), '9a50ddbef4c82eb9003bd496a00e0989')

        def test_response_downloading(self):
            file_path = os.path.join(tempfile.gettempdir(), '1m.data')
            req = HTTPCons()
            req.request("https://static.hellflame.net/resource/c8c12b1c34af9808c34fa60d862016b7")
            resp = SockFeed(req)
            resp.disable_progress = True
            resp.http_response(file_path, overwrite=True)

            with open(file_path, 'rb') as handle:
                content = handle.read()

            os.remove(resp.file_handle.name)
            self.assertEqual(hashlib.md5(content).hexdigest(), '9a50ddbef4c82eb9003bd496a00e0989')

        def test_small_response_in_memory(self):
            req = HTTPCons()
            req.request("https://static.hellflame.net/resource/5573012afe7227ab4457331df42af57d")
            resp = SockFeed(req)
            resp.disable_progress = True
            resp.http_response()
            self.assertEqual(hashlib.md5(resp.data).hexdigest(), '8688229badcaa3cb2730dab99a618be6')

        def test_small_response_downloading(self):
            file_path = os.path.join(tempfile.gettempdir(), '3k.data')
            req = HTTPCons()
            req.request("https://static.hellflame.net/resource/5573012afe7227ab4457331df42af57d")
            resp = SockFeed(req)
            resp.disable_progress = True
            resp.http_response(file_path, overwrite=True)
            with open(file_path, 'rb') as handle:
                content = handle.read()
            os.remove(resp.file_handle.name)
            self.assertEqual(hashlib.md5(content).hexdigest(), '8688229badcaa3cb2730dab99a618be6')

        def test_non_chunked_in_memory(self):
            req = HTTPCons()
            req.request("https://raw.githubusercontent.com/hellflame/qiniu_manager/v1.4.6/qiniuManager/manager.py")
            resp = SockFeed(req)
            resp.disable_progress = True
            resp.http_response()
            self.assertEqual(hashlib.md5(resp.data).hexdigest(), '276efce035d49f7f3ea168b720075523')


    unittest.main(verbosity=2)
