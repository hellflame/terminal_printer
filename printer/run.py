# coding=utf8
from __future__ import print_function
from painter import Printer
from resource import font_handle, missing_font

printer = Printer()

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
                                    epilog="初次使用，需要初始化字体下载，"
                                           "执行 terminalprint -i 初始化")
    parse.add_argument("-i", "--init", action="store_true", help="初始化程序，下载字体")
    parse.add_argument("-t", '--text', default="HellFlame", help="设置将要处理的文本内容，默认为 HellFlame")
    parse.add_argument("-T", '--type', choices=('en', 'cn'), help="指定文本类型")
    parse.add_argument("-m", '--mode', choices=('text', 'color', 'r_color'), help="设置输出模式")
    parse.add_argument("-c", '--color', type=int, choices=range(30, 51), help="设置颜色")
    parse.add_argument("-f", '--filter', type=int, choices=range(1, 57), help="设置打印填充方式")
    parse.add_argument("-F", '--font', help="设置书写字体")

    # 可选的位置参数
    parse.add_argument("picture", nargs="?", help="可选的图片")
    return parse.parse_args(), parse


def command(args, parse):
    pass


def run():
    command(*parser())

def init_program(wanted):
    check = font_handle(font_path, font_list, base_url='http://7xqh1q.dl1.z0.glb.clouddn.com/')
    if check:
        print(check)
    exit(0)
def text_content(wanted):
    default['text'] = wanted
    return ''
def font_type(wanted):
    default['Type'] = wanted
    default['force'] = True
    return ''
def mode_set(wanted):
    default['mode'] = wanted
    return ''
def color_set(wanted):
    default['color'] = wanted
    return ''
def filter_set(wanted):
    default['Filter'] = wanted
    return ''
def font_set(wanted):
    default['font'] = wanted
    return ''


@seeker.seek(extra={'default': '.'})
def pic_handle(wanted):
    if wanted == '.':
        if missing_font(font_path, font_list):
            print('请运行 -i or --init 初始化字体库\n或者-h or --help 帮助')
            default['init'] = True
            return ''
        else:
            return ''
    else:
        if path.exists(wanted):
            default['file'] = wanted
            return ''
        return '米有找到→_→ {} ←_←这个文件的说喵'.format(wanted)


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
    runner()

