# coding=utf8
from __future__ import print_function
import os
import sys
import time
import shutil
from . import http
if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf8")


def font_downloader(base_url, font_name, font_path):
    """
    字体下载
    :param base_url: 下载链接基地址
    :param font_name: 字体名称
    :param font_path: 字体保存路径
    :return:
    """
    downloader = http.HTTPCons()
    downloader.request(base_url + font_name)
    feed = http.SockFeed(downloader)
    start = time.time()
    feed.http_response(os.path.join(font_path, font_name), chunk=4096)

    if not int(feed.status['code']) == 200:
        print("\033[01;31m{}\033[00m not exist !".format(font_name))
        if feed.file_handle and os.path.isfile(feed.file_handle.name):
            os.unlink(feed.file_handle.name)
        return False

    end = time.time()
    size = int(feed.headers.get('Content-Length', 1))
    print("\033[01;31m{}\033[00m downloaded @speed \033[01;32m{}/s\033[00m"
          .format(font_name,
                  http.unit_change(size / (end - start))))
    return True


def font_handle(font_path, font_list, base_url):
    """
    字体下载管理，如果没有缺失字体依然执行，将提示重新下载所有字体
    :param font_path: 字体路径
    :param font_list: 所需字体列表
    :param base_url: 下载基地址
    :return:
    """
    target = [f for f in font_list if not os.path.exists(os.path.join(font_path, f))]
    if not target:
        # 如果字体完整依然执行初始化，则提示删除原有字体目录
        prompt = "当前字体数据完整，是否继续初始化? y/n "
        if sys.version_info.major == 2:
            if not raw_input(prompt).lower().startswith('y'):
                return False
        else:
            if not input(prompt).lower().startswith('y'):
                return False
        shutil.rmtree(font_path)
        target = font_list

    if not os.path.exists(font_path):
        # 创建字体目录
        os.makedirs(font_path)

    print("Start Downloading {} fonts".format(len(target)))
    for font in target:
        font_downloader(base_url, font, font_path)

    print("下载完成")

