# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages


setup(
    name='TerminalPrinter',
    version='1.2.0',
    keywords=('text printer', 'picture printer', 'picture in terminal', 'print picture in terminal'),
    description="文字,字符,图片终端打印, print something in terminal",
    license='Apache License',
    author='hellflame',
    author_email='hellflamedly@gmail.com',
    url='https://github.com/hellflame/terminal_printer',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Text Processing :: General'
    ],
    install_requires=[
        'Pillow',
        'paramSeeker'
    ],
    platforms="linux, Mac Os",
    entry_points={
        'console_scripts': [
            'terminalprint=terminal_printer.runner:runner'
        ]
    }
)


