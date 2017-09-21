# coding=utf8
__author__ = 'hellflame'

from setuptools import setup, find_packages
from printer.painter import __version__, __author__, __url__

setup(
    name='TerminalPrinter',
    version=__version__,
    keywords=('text printer', 'picture printer', 'picture in terminal', 'print picture in terminal'),
    description="terminal printer",
    license='Apache License',
    author=__author__,
    author_email='hellflamedly@gmail.com',
    url=__url__,
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
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'terminalprint=printer.runner:run'
        ]
    }
)


