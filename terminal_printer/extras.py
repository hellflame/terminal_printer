from os.path import exists
from os import makedirs, removedirs, listdir, unlink
from sys import version
if version[0] == '2':
    from urllib2 import urlopen
    import sys
    reload(sys)
    sys.setdefaultencoding("utf8")
else:
    from urllib.request import urlopen


def font_check(font_path, font_list):
    if not exists(font_path):
        makedirs(font_path)
    target = []
    for font in font_list:
        if not exists(font_path + '/{}'.format(font)):
            target.append(font)
    return target


def font_downloader(base_url, font_name, font_path):
    with open(font_path + '/{}'.format(font_name), 'w') as f_handle:
        handle = urlopen(base_url + font_name)
        f_handle.write(handle.read())


def font_handle(font_path, font_list, base_url):
    target = font_check(font_path, font_list)
    if not target:
        print("now delete the old font files\nPlease rerun this command")
        for i in listdir(font_path):
            unlink(font_path + '/' + i)
        removedirs(font_path)

    for font in target:
        print(font + ' is downloading...')
        font_downloader(base_url, font, font_path)
        print(font + ' downloaded~~')


