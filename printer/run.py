# coding=utf8
from __future__ import print_function
import os
import painter
from resource import font_handle, missing_font


def parser():
    import argparse
    parse = argparse.ArgumentParser(description="Terminal Printer",
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog="初次使用，需要初始化字体下载"
                                           "\r\n执行 terminalprint -i 初始化"
                                           "\r\n更多帮助信息请访问: " + painter.__url__)
    parse.add_argument("-i", "--init", action="store_true", help="初始化程序，下载字体")
    parse.add_argument("-t", '--text', default="HellFlame", help="设置将要处理的文本内容，默认为 HellFlame")
    parse.add_argument("-l", '--lang', metavar="l", choices=('en', 'cn'), help="指定语种")
    parse.add_argument("-m", '--mode', metavar="m", choices=('text', 'color', 'r_color'), help="设置输出模式")
    parse.add_argument("-g", '--gray', action="store_true", help="图像转换为灰度图(若指定图)")
    parse.add_argument("-kr", '--keep-ratio', action="store_true", help="保持图片比例")
    parse.add_argument("-c", '--color', type=int, metavar="i", choices=range(30, 51), help="设置颜色")
    parse.add_argument("-f", '--filter', type=int, metavar="i", default=73, choices=range(1, len(painter.MESS_FILTERS)),
                       help="设置打印填充方式")
    parse.add_argument("--width", type=int, default=None, help="设置输出宽度，需要与高度一起设置")
    parse.add_argument("--height", type=int, default=None, help="设置输出高度，需要与宽度一起设置")
    parse.add_argument("-F", '--font', metavar="path", help="设置书写字体")
    parse.add_argument("-r", '--reverse', action="store_true", help="反色(对彩色输出无效)")
    parse.add_argument("-v", '--version', action="store_true", help="输出版本信息")

    # 可选的位置参数
    parse.add_argument("picture", nargs="?", help="可选的图片")
    return parse.parse_args(), parse


def command(args, parse):
    print("\n".join(['{} => {}'.format(k, v) for k, v in args.__dict__.items()]))
    if args.init:
        font_handle(painter.FONT_DIR, painter.FONT_LIST, 'http://7xqh1q.dl1.z0.glb.clouddn.com/')
    elif args.version:
        print("TerminalPrinter v." + painter.__version__)
    elif args.picture:
        if os.path.exists(args.picture):
            print(painter.make_terminal_img(painter.get_img(args.picture, gray=args.gray),
                                            filter_type=args.filter, width=args.width, height=args.height,
                                            dye=args.color, reverse=args.reverse, keep_ratio=args.keep_ratio,
                                            gray=args.gray))
        else:
            print("请输入有效图片路径")
    else:

        pass


def run():
    command(*parser())


if __name__ == '__main__':
    run()

