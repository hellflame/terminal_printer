# coding=utf8
from __future__ import print_function
from painter import FONT_LIST, FONT_DIR, MESS_FILTERS, __version__, __url__
from resource import font_handle, missing_font


default = {"text": "HellFlame",
           "Type": "",
           "mode": "text",
           "color": "31",
           "Filter": 14,
           "font": 0,
           "file": '',
           "force": False,
           'init': False}


def parser():
    import argparse
    parse = argparse.ArgumentParser(description="Terminal Printer",
                                    formatter_class=argparse.RawTextHelpFormatter,
                                    epilog="初次使用，需要初始化字体下载"
                                           "\r\n执行 terminalprint -i 初始化"
                                           "\r\n更多帮助信息请访问: " + __url__)
    parse.add_argument("-i", "--init", action="store_true", help="初始化程序，下载字体")
    parse.add_argument("-t", '--text', default="HellFlame", help="设置将要处理的文本内容，默认为 HellFlame")
    parse.add_argument("-l", '--lang', metavar="l", choices=('en', 'cn'), help="指定语种")
    parse.add_argument("-m", '--mode', metavar="m", choices=('text', 'color', 'r_color'), help="设置输出模式")
    parse.add_argument("-kc", '--keep-color', action="store_true", help="恢复原图颜色(若指定图)")
    parse.add_argument("-c", '--color', type=int, metavar="i", choices=range(30, 51), help="设置颜色")
    parse.add_argument("-f", '--filter', type=int, metavar="i", choices=range(1, len(MESS_FILTERS) - 1), help="设置打印填充方式")
    parse.add_argument("-F", '--font', type=int, metavar="i", help="设置书写字体")
    parse.add_argument("-v", '--version', action="store_true", help="输出版本信息")

    # 可选的位置参数
    parse.add_argument("picture", nargs="?", help="可选的图片")
    return parse.parse_args(), parse


def command(args, parse):
    print(args)
    if args.init:
        font_handle(FONT_DIR, FONT_LIST, 'http://7xqh1q.dl1.z0.glb.clouddn.com/')
    elif args.version:
        print("TerminalPrinter v." + __version__)
    else:
        printer = Printer()



def run():
    command(*parser())


def runner():
    seeker.run(no_output=True)
    if default['init']:
        exit(0)

    if default['file']:
        printer.set_img(default['file'])
        pic_str = printer.make_char_img(filter_type=default['Filter'])

    else:
        if default['Type']:
            auto = False
        else:
            auto = True
        printer.text_drawer(text=default['text'], lang=default['Type'], font_choice=default['font'], auto=auto)
        printer.set_img(printer.tmp_pic)
        pic_str = printer.make_char_img(default['Filter'])

    if default['mode'] == 'color':
        print(printer.dye_all(pic_str, default['color']))
    elif default['mode'] == 'r_color':
        print(printer.dye_rand(pic_str))
    else:
        print(pic_str)


if __name__ == '__main__':
    run()

