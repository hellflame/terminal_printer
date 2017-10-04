# coding=utf8
from __future__ import absolute_import, division, print_function

import os
import fnmatch
import unittest


def get_modules():
    # 只能添加test根目录下的 *_test.py 用例
    modules = []

    for _, _, f in os.walk(os.path.dirname(__file__) or '.'):
        for i in filter(lambda x: fnmatch.fnmatch(x, '*_test.py'), f):
            modules.append('printer.test.' + os.path.basename(i)[:-3])
        break  # just first level

    return modules


def tester(modules):
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromNames(modules))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    tester(get_modules())

