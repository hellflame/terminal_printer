# coding=utf8
from __future__ import print_function
import os
import sys
import shutil
from os.path import exists, join
if sys.version_info.major == 2:
    from urllib2 import urlopen
    reload(sys)
    sys.setdefaultencoding("utf8")
else:
    from urllib.request import urlopen


def font_downloader(base_url, font_name, font_path):
    """
    字体下载
    :param base_url:
    :param font_name:
    :param font_path:
    :return:
    """
    with open(join(font_path, font_name), 'w') as f_handle:
        handle = urlopen(base_url + font_name)
        f_handle.write(handle.read())


def font_handle(font_path, font_list, base_url):
    """
    字体下载管理，如果没有缺失字体依然执行，将提示重新下载所有字体
    :param font_path:
    :param font_list:
    :param base_url:
    :return:
    """
    target = [f for f in font_list if not exists(join(font_path, f))]
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

    if not exists(font_path):
        # 创建字体目录
        os.makedirs(font_path)

    for index, font in enumerate(target):
        print("downloading", '{}/{}'.format(index + 1, len(target)), font)
        font_downloader(base_url, font, font_path)
        sys.stdout.write("\033[F")
    print("下载完成" + ' ' * 20)

