# coding=utf8

import os
import sys
import time
import shutil
from os import path

from PIL import ImageFont

from printer.http import HTTPCons, SockFeed, unit_change

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf8")

# __all__ = ['font_downloader', 'font_handle']

FONT_LIST = ['shuyan.ttf',
             'letter.ttf',
             'Haibaoyuanyuan.ttf',
             'fengyun.ttf',
             'huakangbold.otf']

_font_prefix = "https://raw.githubusercontent.com/hellflame/terminal_printer/" \
               "808004a7cd41b4383bfe6aa310c491c69d9b2556/fonts/"

FONT_URL = {
    f: _font_prefix + f for f in FONT_LIST
}

FONT_DIR = path.join(path.expanduser('~'), ".terminal_fonts")


def choose_font(choice):
    if choice.isdigit():
        choice = int(choice)
        font = path.join(FONT_DIR, FONT_LIST[choice if len(FONT_LIST) - 1 >= choice >= 0 else 0])
    else:
        font = choice
    if not path.exists(font) and path.isfile(font):
        return font, False
    return font, True


def initiate_true_type(choice, size=20):
    font_path, exist = choose_font(choice)
    if not exist:
        print("字体文件不存在({})，请使用其他字体".format(font_path))
        return None
    try:
        return ImageFont.truetype(font_path, size)
    except IOError:
        print("字体文件损坏({})，请使用其他字体".format(font_path))
        return None


def font_downloader(font_link, font_dir):
    """
    字体下载
    :param font_link: 字体名称
    :param font_dir: 字体保存路径
    :return:
    """
    font_name = os.path.basename(font_link)
    save_path = os.path.join(font_dir, font_name)
    downloader = HTTPCons()
    downloader.request(font_link)
    feed = SockFeed(downloader)
    start = time.time()
    feed.http_response(save_path, chunk=4096)
    end = time.time()
    if int(feed.status['code']) == 200:
        size = os.stat(save_path).st_size
        print("\033[01;31m{}\033[00m downloaded @speed \033[01;32m{}/s\033[00m"
              .format(font_name,
                      unit_change(size / (end - start))))
    else:
        print("\033[01;31m{}\033[00m 下载失败".format(font_name))
    return True


def font_init(show_prompt=True):
    """
    字体下载管理，如果没有缺失字体依然执行，将提示重新下载所有字体
    :param show_prompt: 显示提示信息
    :return:
    """
    target = [FONT_URL[f] for f in FONT_URL if not os.path.exists(os.path.join(FONT_DIR, f))]
    if not target:
        # 如果字体完整依然执行初始化，则提示删除原有字体目录
        if show_prompt:
            # 如果不显示提示信息，则直接删除
            prompt = "当前字体数据完整，是否删除后继续初始化? y/n "
            try:
                if sys.version_info.major == 2:
                    if not raw_input(prompt).lower().startswith('y'):
                        return False
                else:
                    if not input(prompt).lower().startswith('y'):
                        return False
            except KeyboardInterrupt:
                exit(0)
        shutil.rmtree(FONT_DIR)
        target = FONT_URL.values()

    if not os.path.exists(FONT_DIR):
        # 创建字体目录
        os.makedirs(FONT_DIR)

    print("Start Downloading {} fonts".format(len(target)))
    for font in target:
        font_downloader(font, FONT_DIR)

    print("下载完成")

