#!/bin/bash
# coding=utf8

from PIL import Image, ImageFont, ImageDraw
from random import randrange
from os import popen
color = '.~-_+*^?/%$!@( #&`\\)|1234567890abcdefghijklmnopqrstuvwxyz'
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# use the absolute path if want to doploy it when you are not @ present directory
location = __file__.replace(__file__.split('/')[-1], 'fonts/')


class Printer:
    def __init__(self):
        self.filter_type = '.~-_+*^?/%$!@( #&`\\)|1234567890abcdefghijklmnopqrstuvwxyz'
        self.font_location = __file__.replace(__file__.split('/')[-1], 'fonts/')
        self.img = None

    def make_char_img(self, filter_type=14):
        if not self.img:
            return False
        pix = self.img.load()
        pic_str = ''
        width, height = self.img.size
        for h in xrange(height):
            for w in xrange(width):
                pic_str += color[int(pix[w, h]) * int(filter_type) / 255]
            pic_str += '\n'
        return pic_str

    def set_img(self, file_path, is_picture=False):
        img = Image.open(file_path)
        w, h = img.size
        console = popen("stty size").read().split()
        console_wid, console_hei = int(console[1]), int(console[0])
        if is_picture:
            img = img.resize((console_wid, h))
        else:
            img = img.resize((console_wid, console_hei))
        self.img = img.convert('L')

    def text_drawer(self, text, lang, font_choice=0):
        text_len = len(text)
        tmp_pic = "/tmp/temp_{}.png".format(popen("echo -n $USER").read())
        if lang == "en":
            fontsize = 20
            font = ((self.font_location + "DejaVuSansMono-Bold.ttf", int(text_len * fontsize * 0.63), int(fontsize * 1.15)),
                    (self.font_location + "handstd_h.otf", int(text_len * fontsize * 0.55), int(fontsize)),
                    (self.font_location + "shuyan.ttf", int(text_len * fontsize * 0.5), int(fontsize * 1.2)),
                    (self.font_location + "fengyun.ttf", int(text_len * fontsize * 0.68), int(fontsize * 1.3))
                    )
        else:
            fontsize = 20
            font = ((self.font_location + "letter.ttf", int(text_len * fontsize), int(fontsize * 1.1)),
                    (self.font_location + "shuyan.ttf", int(text_len * fontsize * 1.05), int(fontsize * 1.2)),
                    (self.font_location + "huakangbold.otf", int(text_len * fontsize), int(fontsize * 1.4)),
                    (self.font_location + "fengyun.ttf", int(text_len * fontsize), int(fontsize * 1.4))
                    )
        Max = 3
        if 0 <= font_choice <= Max:
            font, width, height = font[font_choice]
        elif font_choice > Max:
            font, width, height = font[Max]
        else:
            font, width, height = font[0]
        im = Image.new("1", (width, height), 'white')
        font = ImageFont.truetype(font, fontsize)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), unicode(text), font=font)
        im.save(tmp_pic)
        return tmp_pic

    @staticmethod
    def getlang(text):
        lang_list = []
        for i in text:
            if unichr(ord(i)) == i.decode('utf8', errors='ignore'):
                lang_list.append({
                    'lang': 'en',
                    'content': i
                })
            else:
                lang_list.append({
                    'lang': 'other',
                    'content': i
                })
        char_count = len(lang_list)
        if char_count == 1:
            return lang_list
        result = []
        mark = 0
        for i in range(char_count)[1:]:
            if lang_list[i - 1]['lang'] == lang_list[i]['lang']:
                if i == 1:
                    result.append(lang_list[i - 1])
                    result[mark]['content'] += lang_list[i]['content']
                else:
                    result[mark]['content'] += lang_list[i]['content']
            else:
                if i == 1:
                    result.append(lang_list[i - 1])
                result.append(lang_list[i])
                mark += 1
        return result

    @staticmethod
    def dye(string, color):
        return color + string[1:] + "\033[1;m"

    @staticmethod
    def dye_all(string, color):
        temp = ""
        str_list = string.split("\n")
        for i in str_list:
            temp += paint(i, color)
            if str_list.index(i) != 1:
                temp += "\n"
        return temp

    @staticmethod
    def dye_rand(string):
        temp = ""
        for i in string:
            if i != "\n":
                temp += "\033[{};{}m{}\033[1;m".format(randrange(1, 4), randrange(30, 40), i)
        return temp

    @staticmethod
    def get_color(tail):
        return "\033[3;{}m".format(tail)


def preprocess(img_name, a_file=False):
    img = Image.open(img_name)
    w, h = img.size
    console = popen("stty size").read().split()
    console_wid, console_hei = int(console[1]), int(console[0])
    if not a_file:
        img = img.resize((console_wid, h))
    else:
        img = img.resize((console_wid, console_hei))
    img = img.convert('L')
    return img


def argSeeker(header):
    temp = sys.argv
    for i in temp:
        index = temp.index(i)
        if i == header and not temp[index + 1].startswith("-"):
            return temp[index + 1]
    return False


def make_char_img(img, Filter=14):
    pix = img.load()
    pic_str = ''
    width, height = img.size
    for h in xrange(height):
        for w in xrange(width):
            pic_str += color[int(pix[w, h]) * int(Filter) / 255]
        pic_str += '\n'
    return pic_str


def paint(string, color):
    return color + string[1:] + "\033[1;m"


def paint_all(string, color):
    temp = ""
    str_list = string.split("\n")
    for i in str_list:
        temp += paint(i, color)
        if str_list.index(i) != 1:
            temp += "\n"
    return temp


def paint_rand(string):
    from random import randrange
    temp = ""
    for i in string:
        if i != "\n":
            temp += "\033[{};{}m{}\033[1;m".format(randrange(1, 4), randrange(30, 40), i)
    return temp


def drawer(text, fontsize, color="white", Type="en", choice=0):
    text_len = len(text)
    locate = "/tmp/temp_{}.png".format(popen("echo -n $USER").read())
    if Type == "en":
        font = ((location + "DejaVuSansMono-Bold.ttf", int(text_len * fontsize * 0.63), int(fontsize * 1.15)),
                (location + "handstd_h.otf", int(text_len * fontsize * 0.55), int(fontsize)),
                (location + "shuyan.ttf", int(text_len * fontsize * 0.5), int(fontsize * 1.2)),
                (location + "fengyun.ttf", int(text_len * fontsize * 0.68), int(fontsize * 1.3))
                )
    else:
        font = ((location + "letter.ttf", int(text_len * fontsize), int(fontsize * 1.1)),
                (location + "shuyan.ttf", int(text_len * fontsize * 1.05), int(fontsize * 1.2)),
                (location + "huakangbold.otf", int(text_len * fontsize), int(fontsize * 1.4)),
                (location + "fengyun.ttf", int(text_len * fontsize), int(fontsize * 1.4))
                )
    Max = 3
    if 0 <= choice <= Max:
        font, width, height = font[choice]
    elif choice > Max:
        font, width, height = font[Max]
    else:
        font, width, height = font[0]
    im = Image.new("1", (width, height), color)
    font = ImageFont.truetype(font, fontsize)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), unicode(text), font=font)
    im.save(locate)
    return locate


def main_(text, Type="en", mode="text", color="\033[2;33m", Filter=15, font_choice='0'):
    text = u"{}".format(text)
    draw = drawer(text, 20, Type=Type, choice=int(font_choice))
    img = preprocess(draw)
    pic_str = make_char_img(img, Filter=Filter)
    if mode == "text":
        print(pic_str)
    elif mode == "color":
        print(paint_all(pic_str, color))
    elif mode == "r_color":
        print(paint_rand(pic_str))


def from_file(filename, mode="text", Filter=15):
    try:
        img = preprocess(filename, a_file=True)
        pic_str = make_char_img(img, Filter=Filter)
        if mode == "text":
            print(pic_str)
        elif mode == "color":
            print(paint_all(pic_str, color))
        elif mode == "r_color":
            print(paint_rand(pic_str))
    except IOError:
        print("米有找到→_→ {} ←_←这个文件的说喵～～～".format(filename))
        return False
    except Exception, e:
        print(e)


def getColor(after):
    return "\033[3;{}m".format(after)


def getType(text):
    temp = text
    if 0 <= ord(temp.decode("utf-8")[0]) <= 255:
        return "en"
    return "other"


def main():
    default = {"text": "HellFlame",
               "Type": "en",
               "mode": "text",
               "color": "31",
               "Filter": 14,
               "font": 0,
               }
    keymap = {"text": "-t",
              "Type": "-T",
              "mode": "-m",
              "color": "-c",
              "Filter": "-f",
              "font": "-F",
              }
    mapDesc = {
        "": " 直接输入图片文件名，则对图片进行字符化处理",
        "-t": "设置将要处理的文本内容，默认为{}".format(default["text"]),
        "-T": "强制指定文本类型，默认为系统自动判别，若指定为英文，则 -T en，其他类型时输入其他",
        "-m": "设置输出模式, text表示文本输出；color表示按某种颜色输出，颜色值由-c指定；r_color表示使用随机颜色填充",
        "-c": "若模式选择为color，则指定将要输出的颜色,默认为{},输入值范围为30 ～ 50，不排除某些值没有对应颜色的可能,虽然你也可以输入其他值试一试".format(default["color"]),
        "-f": "设置打印填充方式，可选择1-{}的数值，输出内容的精细程度会随数值的增大而变细致，但这还跟终端窗口的大小以及屏幕分辨率有关，过高的填充值会造成画面破碎"
        .format(color.__len__() - 1),
        "-F": "设置输出字体，结果可能与文本类型有关"
    }
    for i in default:
        temp = argSeeker(keymap[i])
        if temp:
            default[i] = temp
        elif i == "Type":
            seeker = argSeeker("-t")
            if seeker:
                default["Type"] = getType(argSeeker("-t"))
    args = sys.argv
    mark = True
    if args.__len__() >= 2:
        if not args[1].startswith("-"):
            mark = False
            filename = args[1]
            from_file(filename, mode=default["mode"], Filter=default["Filter"])
        elif args[1] == "--help" or args[1] == "-h":
            mark = False
            print "\n*******帮助模式*******\n"
            print("deploy like this\n\n\tterminalprint target.jpg\n\tterminalprint -t testing")
            print("\tterminalprint -t 中文 -m r_color")
            print("\tterminalprint -t linux -m color -c 5")
            print("\tterminalprint -t hellflame -m text -f 3")
            print("\tterminalprint -t linux -F 2 -m r_color")
            print("\n")
            for i in mapDesc:
                print " \t" + i + " ==> " + mapDesc[i]
            print("")
    if mark:
        main_(text=default["text"],
              Type=default["Type"],
              mode=default["mode"],
              color=getColor(default["color"]),
              Filter=default["Filter"],
              font_choice=default["font"])


if __name__ == '__main__':
    main()


