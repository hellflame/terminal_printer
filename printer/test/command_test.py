# coding=utf8
from __future__ import print_function, absolute_import

import shlex
import random
import string
import unittest

from printer.run import *
from printer.painter import MESS_FILTERS, FONT_LIST


class CommandTester(unittest.TestCase):
    def setUp(self):
        _, self.parser = parser()

    @staticmethod
    def gen_rand(length):
        return "".join(random.choice(string.digits + string.ascii_letters + ' ') for _ in range(length))

    def test_init(self):
        self.assertTrue(self.parser.parse_args(['-i']).init)
        self.assertTrue(self.parser.parse_args(['--init']).init)

    def test_text(self):
        name = self.gen_rand(20)
        self.assertEqual(name, self.parser.parse_args(shlex.split("--text '{}'".format(name))).text)
        self.assertEqual(name, self.parser.parse_args(shlex.split("-t '{}'".format(name))).text)
        self.assertEqual('HellFlame', self.parser.parse_args().text)

    def test_color(self):
        color = random.randrange(30, 50)
        self.assertEqual(color, self.parser.parse_args(shlex.split("--color {}".format(color))).color)
        self.assertEqual(color, self.parser.parse_args(shlex.split("-c {}".format(color))).color)

    def test_filter(self):
        f = random.randrange(1, len(MESS_FILTERS))
        self.assertEqual(f, self.parser.parse_args(shlex.split("--filter {}".format(f))).filter)
        self.assertEqual(f, self.parser.parse_args(shlex.split("-f {}".format(f))).filter)
        self.assertEqual(73, self.parser.parse_args().filter)

    def test_width_height(self):
        w, h = random.randrange(1, 100), random.randrange(1, 100)
        parse = self.parser.parse_args(shlex.split("--width {} --height {}".format(w, h)))
        self.assertEqual(w, parse.width)
        self.assertEqual(h, parse.height)

    def test_gray(self):
        self.assertTrue(self.parser.parse_args(['--gray']).gray)
        self.assertTrue(self.parser.parse_args(['-g']).gray)

    def test_keep_ratio(self):
        self.assertTrue(self.parser.parse_args(['--keep-ratio']).keep_ratio)
        self.assertTrue(self.parser.parse_args(['-kr']).keep_ratio)

    def test_font(self):
        f = random.randrange(0, len(FONT_LIST) - 1)
        self.assertEqual(f, self.parser.parse_args(shlex.split('--font {}'.format(f))).font)
        self.assertEqual(f, self.parser.parse_args(shlex.split('-F {}'.format(f))).font)

    def test_reverse(self):
        self.assertTrue(self.parser.parse_args(['-r']).reverse)
        self.assertTrue(self.parser.parse_args(['--reverse']).reverse)


if __name__ == '__main__':
    unittest.main(verbosity=2)


