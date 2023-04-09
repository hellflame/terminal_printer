import os
import platform

from printer.version import __version__
from printer.painter import DEFAULT_SIZE
from printer.font_helper import choose_font


def print_version():
    print("TerminalPrinter v{}".format(__version__))


def print_debug(args):
    print_version()
    print("Shell: {}".format(os.getenv("SHELL")))
    print("Term: {}".format(os.getenv("TERM")))
    print("Platform: {}".format("/".join(platform.uname())))
    print("Given Size: {}/{} Default Size: {}/{}".format(args.width, args.height, *DEFAULT_SIZE))
    print("Arguments: {}".format(" ".join(["{}:{}".format(k, v) for k, v in args.__dict__.items()])))
    if args.text:
        font, exist = choose_font(args.font)
        print("Font: {} (exist? {})".format(font, exist))
