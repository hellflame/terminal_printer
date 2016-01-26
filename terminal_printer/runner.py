# coding=utf8
from paramSeeker import ParamSeeker
from printer import Printer
from extras import font_handle, font_check
from os import path

seeker = ParamSeeker()
printer = Printer()

font_list = ['DejaVuSansMono-Bold.ttf',
             'handstd_h.otf',
             'fengyun.ttf',
             'huakangbold.otf',
             'letter.ttf',
             'shuyan.ttf']

font_path = printer.font_location

default = {"text": "HellFlame",
           "Type": "",
           "mode": "text",
           "color": "31",
           "Filter": 14,
           "font": 0,
           "file": '',
           "force": False,
           'init': False}


@seeker.seek(param='--init', short='-i', is_mark=True, extra={'desc': 'download fonts and init program'})
def init_program(wanted):
    check = font_handle(font_path, font_list, base_url='http://7xqh1q.dl1.z0.glb.clouddn.com/')
    if check:
        print(check)
    exit(0)


@seeker.seek(param='--text', short='-t', extra={'desc': '设置将要处理的文本内容，默认为HellFlame'})
def text_content(wanted):
    default['text'] = wanted
    return ''


@seeker.seek(param='--type', short='-T', extra={'desc': '强制指定文本类型，默认为系统自动判别，若指定为英文，则 -T en，其他类型时输入其他'})
def font_type(wanted):
    default['Type'] = wanted
    default['force'] = True
    return ''


@seeker.seek(param='--mode', short='-m', extra={'desc': '设置输出模式, text表示文本输出；color表示按某种颜色输出，颜色值由-c指定；r_color表示使用随机颜色填充'})
def mode_set(wanted):
    default['mode'] = wanted
    return ''


@seeker.seek(param='--color', short='-c', extra={'desc': "若模式选择为color，则指定将要输出的颜色,默认为{},输入值范围为30 ～ 50，"
                                                         "不排除某些值没有对应颜色的可能,虽然你也可以输入其他值试一试".format(default["color"])})
def color_set(wanted):
    default['color'] = wanted
    return ''


@seeker.seek(param='--filter', short='-f', extra={'desc': "设置打印填充方式，可选择1-56的数值，输出内容的精细程度会随数值的增大而变细致，"
                                                          "但这还跟终端窗口的大小以及屏幕分辨率有关，过高的填充值会造成画面破碎"})
def filter_set(wanted):
    default['Filter'] = wanted
    return ''


@seeker.seek(param='--font', short='-F', extra={'desc': "设置输出字体，结果可能与文本类型有关"})
def font_set(wanted):
    default['font'] = wanted
    return ''


@seeker.seek(extra={'default': '.'})
def pic_handle(wanted):
    if wanted == '.':
        if font_check(font_path, font_list):
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


seeker.set_desc("terminal text or image printer")
seeker.set_usage_desc("terminalprint -[tFmcf] [param,]")
seeker.set_usage_desc("terminalprint picture.jpg")
seeker.set_usage_desc("terminalprint -t linux -m r_color")
seeker.set_usage_desc("terminalprint -t 测试 -m color -c 5")
seeker.set_usage_desc("terminalprint -t 女王大人 -F 1 -m r_color")


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

