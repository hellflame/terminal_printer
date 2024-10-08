# coding=utf8
import sys
import random
import subprocess
from os import popen

from PIL import Image, ImageDraw

from printer.font_helper import initiate_true_type

DEFAULT_SIZE = 50, 30  # width, height
_SIZE_CMD = "stty size"

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding('utf8')
    MESS_FILTERS = ''.join([unichr(i) for i in range(32, 256)])
else:
    MESS_FILTERS = ''.join([chr(i) for i in range(32, 256)])
    unicode = lambda s: s

try:
    _code, _output = subprocess.getstatusoutput(_SIZE_CMD)
    if _code == 0:
        DEFAULT_SIZE = [int(s) for s in _output.split(' ')][::-1]
except AttributeError:  # python2
    try:
        DEFAULT_SIZE = [int(s) for s in popen(_SIZE_CMD).read().split(' ')][::-1]
    except:
        pass

get_text_size = getattr(ImageDraw.ImageDraw, 'textsize', None)
if not get_text_size:
    # for pillow version >= 10.0.0
    def get_text_size(self, txt, font):
        _, _, x, y = ImageDraw.ImageDraw.textbbox(self, (0, 0), txt, font)
        return x, y


class ImageMap(object):
    def __init__(self):
        self._image = {}

    def __setitem__(self, key, value):
        self._image[key] = value

    def __getitem__(self, key):
        return self._image[key]


def make_terminal_img(img, filter_type=None, width=None,
                      height=None, dye=None, reverse=False,
                      keep_ratio=False, gray=True, strip_white=False):
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
    :param strip_white: 是否删除(文字打印)模式下的空白行
    :return: 图像字符
    """
    if not img:
        # 如果文字画布生成失败，img为空
        return ''
    if not keep_ratio:
        img = img.resize((width or DEFAULT_SIZE[0], height or DEFAULT_SIZE[1]))
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

    if strip_white:
        image_map = ImageMap()
        white_lines = 0
        after_h = 0
        is_start_line = True
        for h in range(height):
            if all([pix[w, h] == 255 for w in range(width)]):
                if is_start_line:
                    # skip first white line
                    is_start_line = False
                elif h == height - 2:
                    # skip last white line
                    pass
                else:
                    white_lines += 1
                    continue
            for w in range(width):
                image_map[w, after_h] = pix[w, h]
            after_h += 1
        height = after_h
        pix = image_map

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
        result = '\033[01;{}m'.format(dye) + \
                 '\n'.join([''.join([render_pix(w, h) for w in range(width)])
                            for h in range(height)]) + '\033[00m'
    elif type(dye) is str:
        # 随机颜色绘制
        result = '\n'.join([''.join(["\033[01;{}m{}".format(random.randrange(30, 40),
                                                            render_pix(w, h))
                                     for w in range(width)])
                            for h in range(height)]) + '\033[00m'

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
    font = initiate_true_type(fonts, 20)
    if not font:
        return None
    txt = unicode(text)
    text_size = get_text_size(draw, txt, font=font)
    im = im.resize(text_size)

    draw = ImageDraw.Draw(im)
    draw.text((0, 0), txt, font=font)
    return im

