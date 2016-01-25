from paramSeeker import ParamSeeker
from terminal_printer import font_handle
from os import environ

seeker = ParamSeeker()

font_list = ['DejaVuSansMono-Bold.ttf',
             'handstd_h.otf',
             'fengyun.ttf',
             'huakangbold.otf',
             'letter.ttf',
             'shuyan.ttf']

font_path = environ['HOME']


@seeker.seek(param='--init', short='-i', is_mark=True)
def init_program(wanted):
    check = font_handle(font_path, font_list, base_url='http://7xqh1q.dl1.z0.glb.clouddn.com/')
    if check:
        print(check)
    exit(0)


