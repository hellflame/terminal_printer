# coding=utf8
import sys
import random
from os import popen, path

from PIL import Image, ImageFont, ImageDraw


__author__ = 'hellflame'
__version__ = '1.5.0'
__url__ = 'https://github.com/hellflame/terminal_printer'


FONT_LIST = ['shuyan.ttf',
             'letter.ttf',
             'Haibaoyuanyuan.ttf',
             'fengyun.ttf',
             'huakangbold.otf']

_font_prefix = "https://raw.githubusercontent.com/hellflame/terminal_printer/" \
               "808004a7cd41b4383bfe6aa310c491c69d9b2556/fonts/"

FONT_URL = {
    f: _font_prefix + f for f in FONT_LIST
}

FONT_DIR = path.join(path.expanduser('~'), ".terminal_fonts")


if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    MESS_FILTERS = ''.join([unichr(i) for i in range(32, 256)])
else:
    MESS_FILTERS = ''.join([chr(i) for i in range(32, 256)])
    unicode = lambda s: s

try:
    DEFAULT_SIZE = tuple(reversed([int(s) for s in popen("stty size").read().split()]))
except:
    DEFAULT_SIZE = 50, 30  # width, height


def make_terminal_img(img, filter_type=None, width=None,
                      height=None, dye=None, reverse=False,
                      keep_ratio=False, gray=True):
    """
    在终端输出字符图片
    :param img: 图像
    :param filter_type: 填充字符
    :param width: 输出宽度
    :param height: 输出高度
    :param dye: 上色
    :param reverse: 是否反色
    :param keep_ratio: 是否保持比例
    :param gray: 如果处理图片，是否转换为灰度图
    :return: 图像字符
    """
    if not img:
        # 如果文字画布生成失败，img为空
        return ''
    if not keep_ratio:
        if width is None or height is None:
            img = img.resize(DEFAULT_SIZE)
        else:
            img = img.resize((width, height))
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

    if gray:
        def render_pix(x, y):
            if filter_type:
                if reverse:
                    return MESS_FILTERS[(255 - pix[x, y]) * filter_type // 255]
                return MESS_FILTERS[pix[x, y] * filter_type // 255]
            else:
                if reverse:
                    return MESS_FILTERS[(255 - pix[x, y]) * 4 // 255]
                return MESS_FILTERS[pix[x, y] * 4 // 255]
    else:
        def render_pix(x, y):
            # 如果这里也用和灰度图一样的处理方法的话，会显得很乱，终端中的颜色也难以显示出来
            return '\033[0;38;2;%s;%s;%sm' % pix[x, y][:3] + MESS_FILTERS[filter_type]

    if type(dye) is int:
        # 特定颜色绘制
        result = '\033[01;{}m'.format(dye) + '\n'.join([''.join([render_pix(w, h) for w in range(width)])
                                                        for h in range(height)])
    elif type(dye) is str:
        # 随机颜色绘制
        result = '\n'.join([''.join(["\033[01;{}m{}".format(random.randrange(30, 40),
                                                            render_pix(w, h))
                                     for w in range(width)])
                            for h in range(height)])

    else:
        # 黑白
        result = '\n'.join([''.join([render_pix(w, h)
                                     for w in range(width)])
                            for h in range(height)])
    img.close()
    return result + '\033[00m'


def get_img(file_path, gray=False):
    """
    获取输入图片
    :param file_path: 图片文件位置
    :param gray: 是否转换为灰度图
    :return: img
    """
    try:
        img = Image.open(file_path)
        if gray:
            img = img.convert('L')
        return img
    except Exception:
        print("不支持的图片格式")
        return None


def text_drawer(text, fonts=None):
    """
    将文字书写在白色画布上
    :param text: 要书写的文字
    :param fonts: 字体选择，索引或路径
    :return: img
    """
    im = Image.new("1", (1, 1), 'white')  # 初始画布大小没有关系
    draw = ImageDraw.Draw(im)
    if type(fonts) is int:
        font = path.join(FONT_DIR, FONT_LIST[fonts if len(FONT_LIST) - 1 >= fonts >= 0 else 0])
        # print(font)
    elif fonts is None:
        font = path.join(FONT_DIR, FONT_LIST[0])
    else:
        font = fonts

    try:
        font = ImageFont.truetype(font, 20)
    except IOError:
        print("字体文件损坏，请使用其他字体或重新初始化")
        return None
    except:
        target = path.join(FONT_DIR, FONT_LIST[0])
        if path.exists(target):
            font = ImageFont.truetype(target, 20)
        else:
            print("字体缺失，请初始化字体!")
            return None

    text_size = draw.textsize(unicode(text), font=font)
    im = im.resize(text_size)

    draw = ImageDraw.Draw(im)
    draw.text((0, 0), unicode(text), font=font)
    return im

