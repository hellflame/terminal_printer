# coding=utf8

import os
import argparse

from printer.version import __url__
from printer.painter import MESS_FILTERS, make_terminal_img, text_drawer, get_img
from printer.font_helper import font_init, choose_font
from printer.utils import print_version, print_debug

__all__ = ['parser']


def command(args, parse):
    if args.debug:
        print_debug(args)
    if args.init:
        font_init()
    elif args.version:
        print_version()
    elif args.picture:
        pic_path = args.picture
        if os.path.exists(pic_path) and os.path.isfile(pic_path):
            print(make_terminal_img(
                get_img(pic_path, gray=args.gray),
                filter_type=args.filter, width=args.width, height=args.height,
                dye=args.color, reverse=args.reverse, keep_ratio=args.keep_ratio,
                gray=args.gray))
        else:
            print("请输入有效图片路径")
    elif args.text:
        print(make_terminal_img(
            text_drawer(args.text, args.font),
            filter_type=args.filter, width=args.width, height=args.height,
            dye=args.color, reverse=not args.reverse, keep_ratio=False, gray=True,
            strip_white=True))
    else:
        parse.print_help()


def parser():
    parse = argparse.ArgumentParser(description="Terminal Printer",
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog="首次进行文字处理\r\n"
                                           "需要执行 terminalprint -i 初始化或指定字体\r\n"
                                           "更多帮助信息请参考: " + __url__)

    def usable_color(s):
        _COLOR_MAP = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
                      'magenta': 35, 'cyan': 36, 'white': 37}
        for k, v in _COLOR_MAP.items():
            _COLOR_MAP['bg-' + k] = v + 10
        if s.isdigit():
            if 30 <= int(s) <= 50:
                return int(s)
            raise argparse.ArgumentTypeError("颜色值若为数字，应在30～50之间")
        else:
            return _COLOR_MAP.get(s, s)

    def usable_filter(s):
        if s.isdigit() and 1 <= int(s) <= len(MESS_FILTERS) - 1:
            return int(s)
        raise argparse.ArgumentTypeError("填充方式索引值应在1～{}之间".format(len(MESS_FILTERS) - 1))

    def usable_font(s):
        f, exist = choose_font(s)
        if not exist:
            raise argparse.ArgumentTypeError("字体路径不存在，请检查路径或使用数字")
        return f

    basic = parse.add_argument_group("basics")
    basic.add_argument("-i", "--init", action="store_true", help="初始化程序，下载字体")
    basic.add_argument("-v", '--version', action="store_true", help="输出版本信息")
    basic.add_argument("--debug", action="store_true", help="输出调试信息")

    picture = parse.add_argument_group("pictures")
    picture.add_argument("picture", nargs="?", help="可选的图片")
    picture.add_argument("-kr", '--keep-ratio', action="store_true", help="保持图片比例")

    text = parse.add_argument_group("text")
    text.add_argument("-t", '--text', default="HellFlame", help="设置将要处理的文本内容，默认为 HellFlame")
    text.add_argument("-c", '--color', type=usable_color, metavar="i", help="设置颜色")
    text.add_argument("-g", '--gray', action="store_true", help="图像转换为灰度图(若指定图)")
    text.add_argument("-F", '--font', metavar="path", type=usable_font, default='0', help="设置书写字体")
    text.add_argument("-r", '--reverse', action="store_true", help="反色(对彩色输出无效)")

    common = parse.add_argument_group("common")
    common.add_argument('-W', "--width", metavar="w", type=int, help="设置输出宽度，需要与高度一起设置")
    common.add_argument('-H', "--height", metavar="h", type=int, help="设置输出高度，需要与宽度一起设置")
    common.add_argument("-f", '--filter', type=usable_filter, metavar="i", default=73, help="设置打印填充方式")

    # 可选的位置参数
    return parse.parse_args(), parse


def run():
    command(*parser())


if __name__ == '__main__':
    run()

