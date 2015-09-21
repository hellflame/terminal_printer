# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages

with open('README') as f:
    long_desc = f.read()

setup(
    name='TerminalPrinter',
    version='0.9.4.6',
    keywords=('text printer', 'picture printer', 'picture in terminal', 'print picture in terminal'),
    description="文字,字符,图片终端打印, print something in terminal",
    long_description=long_desc,
    license='MIT',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url='https://github.com/hellflame/terminal_printer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7'
    ],
    include_pakage_data=True,
    pakage_data={
        'data': [
            'data/DejaVuSansMono-Bold.ttf',
            'data/fengyun.ttf',
            'data/handstd_h.otf',
            'data/huakangbold.otf',
            'data/letter.ttf',
            'data/shuyan.ttf'
        ]
    },
    platforms="linux, Mac Os X",
    entry_points={
        'console_scripts': [
            'terminalprint=terminal_printer.terminal_printer:main'
        ]
    }
)


