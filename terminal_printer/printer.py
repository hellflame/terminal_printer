#!/bin/bash
# coding=utf8

from PIL import Image, ImageFont, ImageDraw
from random import randrange
from os import popen, environ


class Printer:
    def __init__(self):
        self.filter_type = '.~-_+*^?/%$!@( #&`\\)|1234567890abcdefghijklmnopqrstuvwxyz'
        self.font_location = environ['HOME'] + '/fonts/'
        self.img = None
        self.tmp_pic = '/tmp/printer_{}.png'.format(environ['USER'])

    def make_char_img(self, filter_type=14):
        if not self.img:
            return False
        pix = self.img.load()
        pic_str = ''
        width, height = self.img.size
        for h in xrange(height):
            for w in xrange(width):
                pic_str += self.filter_type[int(pix[w, h]) * int(filter_type) / 255]
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
        tmp_pic = self.tmp_pic
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
        return color + string + "\033[1;m"

    def dye_all(self, string, color):
        temp = ""
        str_list = string.split("\n")
        for i in str_list:
            temp += self.dye(i, color)
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



