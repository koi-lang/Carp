#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""""

import antlr4

from KoiLexer import KoiLexer
from KoiParser import KoiParser
from koi_interpreter import KoiInterpreter

if __name__ == "__main__":
    lexer = KoiLexer(antlr4.FileStream("examples/Koi/inputs.koi"))
    stream = antlr4.CommonTokenStream(lexer)
    parser = KoiParser(stream)
    tree = parser.program()

    interpret = KoiInterpreter()
    walker = antlr4.ParseTreeWalker()
    walker.walk(interpret, tree)
