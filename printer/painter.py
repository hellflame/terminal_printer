# coding=utf8
from __future__ import print_function
from PIL import Image, ImageFont, ImageDraw
from random import randrange
from os import popen, path
import sys
import string
import tempfile
import getpass

__all__ = ['Printer']
__author__ = 'hellflame'
__version__ = '1.2.0'
__url__ = 'https://github.com/hellflame/terminal_printer'

FONT_LIST = ['DejaVuSansMono-Bold.ttf',
             'handstd_h.otf',
             'fengyun.ttf',
             'huakangbold.otf',
             'letter.ttf',
             'shuyan.ttf']

FONT_DIR = path.join(path.expanduser('~'), ".terminal_fonts")
PIC_TMP = path.join(tempfile.gettempdir(), "printer_{}.png".format(getpass.getuser()))
MESS_FILTERS = string.digits + string.ascii_letters + string.punctuation

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

try:
    DEFAULT_SIZE = [int(s) for s in popen("stty size").read().split()]
except:
    DEFAULT_SIZE = 30, 50  # height, width


def make_char_img(img, filter_type=14):
    if not img:
        return False
    pix = img.load()
    width, height = img.size
    return ''.join(['\n'.join([MESS_FILTERS[int(pix[w, h]) * int(filter_type) / 255]
                               for w in range(width)])
                    for h in range(height)])


def get_gray_img(file_path, width=None, height=None):
    img = Image.open(file_path)
    if width is not None and height is not None:
        img = img.resize((width, height))
    img = img.convert('L')
    img.save(PIC_TMP)


def get_colored_img(file_path, width, height):
    img = Image.open(file_path)
    if width is not None and height is not None:
        img = img.resize((width, height))
    img.save(PIC_TMP)


def text_drawer(text, width, height, font_choice=0):
    """
    将文字书写在画布上
    :param text:
    :param width:
    :param height:
    :param font_choice:
    :return:
    """
    im = Image.new("1", (width, height), 'white')
    draw = ImageDraw.Draw(im)
    size = 20

    def font_location(f):
        return path.join(FONT_DIR, f)

    Max = 3
    if 0 <= font_choice <= Max:
        font, width, height = font[font_choice]
    elif font_choice > Max:
        font, width, height = font[Max]
    else:
        font, width, height = font[0]

    font = font_location('shuyan.ttf')
    font = ImageFont.truetype(font, size)
    text_size = draw.textsize(unicode(text), font=font)
    print(text_size, width, height)
    im = im.resize(text_size)

    draw = ImageDraw.Draw(im)
    draw.text((0, 0), unicode(text), font=font)
    im.save(PIC_TMP)
    print(PIC_TMP)


def simple_lang(text):
    for i in text:
        if unichr(ord(i)) != i.decode('utf8', errors='ignore'):
            return 'other'
    return 'en'


def dye_all(raw_img_string, color):
    return '\033[01;{}m'.format(color) + raw_img_string + '\033[1;m'


def dye_rand(raw_img_string):
    temp = ""
    for i in raw_img_string:
        if i != "\n":
            temp += "\033[{};{}m{}\033[1;m".format(randrange(1, 4), randrange(30, 40), i)

    return temp


if __name__ == '__main__':
    # text_drawer('中文好吧，，貌似是有一点点问题的样子', 200, 100)
    get_colored_img("/Users/hellflame/Downloads/lifecycle.png", 6,6)

