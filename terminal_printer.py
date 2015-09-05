#!/usr/bin/python
# coding=utf8

import Image, os, ImageFont, ImageDraw
color = '.~-_+*^?/%$!@( #&`\\)|1234567890abcdefghijklmnopqrstuvwxyz'
import sys
reload(sys)
sys.setdefaultencoding("utf8")

# use the absolute path if want to doploy it when you are not @ present directory
location = "./"


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


def preprocess(img_name, a_file=False):
    img = Image.open(img_name)
    w, h = img.size
    console = os.popen("stty size").read().split()
    console_wid, console_hei = int(console[1]), int(console[0])
    if not a_file:
        img = img.resize((console_wid, h))
    else:
        img = img.resize((console_wid, console_hei))
    img = img.convert('L')
    return img


def drawer(text, fontsize, color="white", Type="en", choice=0):
    text_len = len(text)
    locate = "/tmp/temp_{}.png".format(os.popen("echo -n $USER").read())
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


def main(text, Type="en", mode="text", color="\033[2;33m", Filter=15, font_choice='0'):
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

if __name__ == '__main__':

    default = {"text": "Flame",
               "Type": "en",
               "mode": "text",
               "color": "31",
               "Filter": 14,
               "font": 0,
               }
    origin = default
    keymap = {"text": "-t",
              "Type": "-T",
              "mode": "-m",
              "color": "-c",
              "Filter": "-f",
              "font": "-F",
              }
    mapDesc = {
        "": " <== 直接输入图片文件名，则对图片进行字符化处理",
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
            for i in mapDesc:
                print "  " + i + " ==> " + mapDesc[i]
    if mark:
        main(text=default["text"],
             Type=default["Type"],
             mode=default["mode"],
             color=getColor(default["color"]),
             Filter=default["Filter"],
             font_choice=default["font"])
