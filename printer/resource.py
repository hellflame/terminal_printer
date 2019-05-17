# coding=utf8
import os
import sys
import time
import shutil

from printer.http import HTTPCons, SockFeed, unit_change

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("utf8")

__all__ = ['font_downloader', 'font_handle']


def font_downloader(font_link, font_dir):
    """
    字体下载
    :param font_link: 字体名称
    :param font_dir: 字体保存路径
    :return:
    """
    font_name = font_link.split("/")[-1]
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


def font_handle(font_dir, fonts_url, show_prompt=True):
    """
    字体下载管理，如果没有缺失字体依然执行，将提示重新下载所有字体
    :param font_dir: 字体路径
    :param fonts_url: 字体链接
    :param show_prompt: 显示提示信息
    :return:
    """
    target = [fonts_url[f] for f in fonts_url if not os.path.exists(os.path.join(font_dir, f))]
    if not target:
        # 如果字体完整依然执行初始化，则提示删除原有字体目录
        if show_prompt:
            # 如果不显示提示信息，则直接删除
            prompt = "当前字体数据完整，是否继续初始化? y/n "
            try:
                if sys.version_info.major == 2:
                    if not raw_input(prompt).lower().startswith('y'):
                        return False
                else:
                    if not input(prompt).lower().startswith('y'):
                        return False
            except KeyboardInterrupt:
                exit(0)
        shutil.rmtree(font_dir)
        target = fonts_url.values()

    if not os.path.exists(font_dir):
        # 创建字体目录
        os.makedirs(font_dir)

    print("Start Downloading {} fonts".format(len(target)))
    for font in target:
        font_downloader(font, font_dir)

    print("下载完成")


if __name__ == '__main__':
    from printer import painter
    font_handle(painter.FONT_DIR, painter.FONT_URL, show_prompt=False)


