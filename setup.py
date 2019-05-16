# coding=utf8

from setuptools import setup
from printer.painter import __version__, __author__, __url__

setup(
    name='TerminalPrinter',
    version=__version__,
    keywords=('字符画', '终端打印'),
    description="终端图片、文字生成器",
    license='MIT',
    author=__author__,
    author_email='hellflamedly@gmail.com',
    url=__url__,
    packages=["printer"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        "Operating System :: MacOS",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        'Topic :: Text Processing :: General',
        'Topic :: Terminals',
        'Topic :: Games/Entertainment'
    ],
    install_requires=[
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'terminalprint=printer.run:run'
        ]
    }
)


