# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages

setup(
    name='TerminalPrinter',
    version='0.9.2',
    keywords=('text printer', 'picture printer', 'picture in terminal', 'print picture in terminal'),
    description="文字,字符,图片终端打印, print something in terminal",
    license='MIT',
    author=__author__,
    author_email='hellflamedly@gmail.com',
    url='https://github.com/hellflame/terminal_printer',
    packages=find_packages(),
    platforms="linux, Mac Os X",
    entry_points={
        'console_scripts': [
            'terminalprint=terminal_printer.terminal_printer.main'
        ]
    }
)


