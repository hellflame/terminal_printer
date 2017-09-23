# coding=utf8
from __future__ import print_function
from PIL import Image, ImageFont, ImageDraw
from os import popen, path
import sys
import random
import getpass
import tempfile

__all__ = ['Printer']
__author__ = 'hellflame'
__version__ = '1.2.0'
__url__ = 'https://github.com/hellflame/terminal_printer'

FONT_LIST = ['shuyan.ttf',
             'letter.ttf',
             'Haibaoyuanyuan.ttf']

FONT_DIR = path.join(path.expanduser('~'), ".terminal_fonts")
PIC_TMP = path.join(tempfile.gettempdir(), "printer_{}.png".format(getpass.getuser()))
# print(PIC_TMP)
MESS_FILTERS = ''.join([unichr(i) for i in range(32, 256)])


if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')

try:
    DEFAULT_SIZE = tuple(reversed([int(s) for s in popen("stty size").read().split()]))
except:
    DEFAULT_SIZE = 50, 30  # width, height


def make_terminal_img(img, filter_type=None, width=None,
                      height=None, dye=None, reverse=False,
                      keep_ratio=False, gray=True):
    """
    在终端输出字符图片
    :param img:
    :param filter_type:
    :param width:
    :param height:
    :param dye:
    :param reverse:
    :return:
    """
    if not img:
        return False
    if not keep_ratio:
        if width is None or height is None:
            img = img.resize(DEFAULT_SIZE)
        else:
            img = img.resize((height, width))
    else:
        size = img.size
        if width is None or height is None:
            ratio = min(float(DEFAULT_SIZE[0]) / size[0], float(DEFAULT_SIZE[1]) / size[1])
            img = img.resize((int(size[0] * ratio), int(size[1] * ratio)))
        else:
            ratio = min(float(width) / size[0], float(height) / size[1])
            img = img.resize((int(size[0] * ratio), int(size[1] * ratio)))
    width, height = img.size
    pix = img.load()

    img.save("./t.png")

    if gray:
        def render_pix(x, y):
            if filter_type:
                if reverse:
                    return MESS_FILTERS[(255 - pix[x, y]) * filter_type // 255]
                return MESS_FILTERS[pix[x, y] * filter_type // 255]
            else:
                if reverse:
                    return MESS_FILTERS[(255 - pix[x, y]) * (len(MESS_FILTERS) - 1) // 255]
                return MESS_FILTERS[pix[x, y] * (len(MESS_FILTERS) - 1) // 255]
    else:
        def render_pix(x, y):
            print(pix[x, y])
            return 'a'

    if type(dye) is int:
        # 特定颜色绘制
        result = '\033[01;{}m'.format(dye) + '\n'.join([''.join([render_pix(w, h) for w in range(width)])
                                                        for h in range(height)]) \
               + '\033[1;m'
    elif type(dye) is str:
        # 随机颜色绘制
        result = '\n'.join([''.join(["\033[{};{}m{}\033[1;m".format(random.randrange(1, 4),
                                                                    random.randrange(30, 40),
                                                                    render_pix(w, h))
                                     for w in range(width)])
                            for h in range(height)])

    else:
        # 黑白
        result = '\n'.join([''.join([render_pix(w, h)
                                     for w in range(width)])
                            for h in range(height)])
    img.close()
    return result


def get_img(file_path, gray=False):
    """
    获取输入图片
    :param file_path:
    :param gray:
    :return:
    """
    img = Image.open(file_path)
    if gray:
        img = img.convert('L')
    return img


def text_drawer(text, fonts=None):
    """
    将文字书写在画布上
    :param text:
    :param fonts:
    :return:
    """
    im = Image.new("1", (1, 1), 'white')
    draw = ImageDraw.Draw(im)
    if type(fonts) is int:
        font = path.join(FONT_DIR, FONT_LIST[fonts if len(FONT_LIST) - 1 >= fonts >= 0 else 0])
        print(font)
    elif fonts is None:
        font = path.join(FONT_DIR, FONT_LIST[0])
    else:
        font = fonts

    try:
        font = ImageFont.truetype(font, 20)
    except:
        font = ImageFont.truetype(path.join(FONT_DIR, FONT_LIST[0]), 20)

    text_size = draw.textsize(unicode(text), font=font)
    im = im.resize(text_size)

    draw = ImageDraw.Draw(im)
    draw.text((0, 0), unicode(text), font=font)
    return im


if __name__ == '__main__':
    a = text_drawer('flame中文')
    a = get_img("/Users/hellflame/Pictures/EvJIITe.jpg")
    result = make_terminal_img(a, dye=34, filter_type=5, gray=False)
    print(result)
    # print(ret_type('file')(text_drawer)("中文测试", 200, 100))
    # test()
    # get_colored_img("/Users/hellflame/Downloads/lifecycle.png", 6,6)

