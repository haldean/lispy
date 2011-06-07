#!/usr/bin/env python

import lispylex
import lispyenv
import lispyacc

import ply.yacc as yacc
import sys

lexer = lispylex.lexer()
parser = lispyacc.parser()

s = sys.stdin.read()
result = parser.parse(s)
result.evaluate(lispyenv.LispyEnv())
