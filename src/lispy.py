#!/usr/bin/env python

import lispylex
import lispyenv
import lispyacc

import ply.yacc as yacc
import sys

lexer = lispylex.lexer()
parser = lispyacc.parser()

if '-i' in sys.argv:
    while True:
        try:
            line = raw_input('> ')
        except EOFError:
            break
        if line == '(quit)':
            break
        parser.parse(line).evaluate(lispyenv.LispyEnv())
else:
    s = sys.stdin.read()
    result = parser.parse(s)
    result.evaluate(lispyenv.LispyEnv())
