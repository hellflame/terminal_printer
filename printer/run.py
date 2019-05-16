# coding=utf8
import os
import argparse

from printer.painter import __url__, __version__, MESS_FILTERS, FONT_LIST, FONT_DIR, \
    FONT_URL, make_terminal_img, text_drawer, get_img

from printer.resource import font_handle

__all__ = ['parser']


def command(args, parse):
    if args.init:
        font_handle(FONT_DIR, FONT_URL)
    elif args.version:
        print("TerminalPrinter v{}".format(__version__))
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
            dye=args.color, reverse=not args.reverse, keep_ratio=False, gray=True))
    else:
        parse.print_help()


def parser():
    parse = argparse.ArgumentParser(description="Terminal Printer",
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog="初次使用，需要初始化字体下载"
                                           "\r\n执行 terminalprint -i 初始化"
                                           "\r\n更多帮助信息请访问: " + __url__)

    def usable_color(s):
        if s.isdigit():
            if 30 <= int(s) <= 50:
                return int(s)
            raise argparse.ArgumentTypeError("颜色值若为数字，应在30～50之间")
        else:
            return s

    def usable_filter(s):
        if s.isdigit() and 1 <= int(s) <= len(MESS_FILTERS) - 1:
            return int(s)
        raise argparse.ArgumentTypeError("填充方式索引值应在1～{}之间".format(len(MESS_FILTERS) - 1))

    def usable_font(s):
        if s.isdigit():
            if 0 <= int(s) <= len(FONT_LIST) - 1:
                return int(s)
            raise argparse.ArgumentTypeError("字体若为数字，应在0～{}之间".format(len(FONT_LIST) - 1))
        else:
            if os.path.exists(s):
                return s
            raise argparse.ArgumentTypeError("字体路径不存在，请检查路径或使用数字")

    basic = parse.add_argument_group("basics")
    basic.add_argument("-i", "--init", action="store_true", help="初始化程序，下载字体")
    basic.add_argument("-v", '--version', action="store_true", help="输出版本信息")

    picture = parse.add_argument_group("pictures")
    picture.add_argument("picture", nargs="?", help="可选的图片")
    picture.add_argument("-kr", '--keep-ratio', action="store_true", help="保持图片比例")

    text = parse.add_argument_group("text")
    text.add_argument("-t", '--text', default="HellFlame", help="设置将要处理的文本内容，默认为 HellFlame")
    text.add_argument("-c", '--color', type=usable_color, metavar="i", help="设置颜色")
    text.add_argument("-g", '--gray', action="store_true", help="图像转换为灰度图(若指定图)")
    text.add_argument("-F", '--font', metavar="path", type=usable_font, help="设置书写字体")
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

