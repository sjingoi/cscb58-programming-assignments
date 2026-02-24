#!/usr/bin/python3
import sys
from codetypes import *

def assembleWords(code: list[Code], out = sys.stdout.buffer):
    """ Assembles a List of Code objects to the target file. """
    for c in code:
        match c:
            case Word(v):
                if -2**31 <= v <= 2**32 - 1:
                    out.write(bytes((v >> i*8) & 0xff for i in (0, 1, 2, 3)))
                else:
                    raise Exception("Word({0}) is out of range".format(v))
