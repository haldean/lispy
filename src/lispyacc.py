from lispycode import *
from lispylex import tokens
import lispyenv
import ply.yacc as yacc

def parser():
    env = lispyenv.LispyEnv()

    def p_sexpseq(t):
        'sexpseq : sexps'
        t[0] = PrognEval(t[1])

    def p_sexps(t):
        '''sexps : sexps sexp
                 | sexp'''
        if len(t) == 3:
            t[0] = t[1] + [t[2]]
        else:
            t[0] = [t[1]]

    def p_sexp(t):
        '''sexp : setq
                | if
                | cond
                | literal
                | symbol
                | defun
                | let
                | progn
                | when
                | unless
                | list'''
        t[0] = t[1]

    def p_when(t):
        'when : LPAREN WHEN sexp sexpseq RPAREN'
        t[0] = IfEval(t[3], t[4], NilEval())

    def p_unless(t):
        'unless : LPAREN UNLESS sexp sexpseq RPAREN'
        t[0] = IfEval(t[3], NilEval(), t[4])

    def p_progn(t):
        'progn : LPAREN PROGN sexpseq RPAREN'
        t[0] = t[3]

    def p_let(t):
        'let : LPAREN LET LPAREN pairlist RPAREN sexpseq RPAREN'
        t[0] = LetEval(t[4], t[6])

    def p_defun(t):
        'defun : LPAREN DEFUN SYMBOL LPAREN defun_args RPAREN sexpseq RPAREN'
        t[0] = DefunEval(t[3], t[5], t[7])

    def p_defun_args(t):
        '''defun_args : SYMBOL defun_args 
                      | '''
        if len(t) > 1:
            t[0] = [t[1]] + t[2]
        else:
            t[0] = []

    def p_cond(t):
        'cond : LPAREN COND LPAREN pairlist RPAREN RPAREN'
        t[0] = CondEval(t[4])

    def p_pairlist(t):
        '''pairlist : pair pairlist
                      | pair'''
        if len(t) == 3:
            t[0] = [t[1]] + t[2]
        else:
            t[0] = [t[1]]

    def p_list_pair(t):
        'pair : LPAREN sexp sexp RPAREN'
        t[0] = (t[2], t[3])

    def p_setq(t):
        'setq : LPAREN SETQ SYMBOL sexp RPAREN'
        t[0] = SetqEval(t[3], t[4])

    def p_if(t):
        'if : LPAREN IF sexp sexp sexp RPAREN'
        t[0] = IfEval(t[3], t[4], t[5])

    def p_list(t):
        'list : LPAREN exprs RPAREN'
        t[0] = ListEval(t[2])

    def p_exprs(t):
        '''exprs : sexp exprs 
                 | sexp'''
        if len(t) == 3:
            t[0] = t[2]
        else:
            t[0] = []
        t[0].insert(0, t[1])

    def p_eval_sym(t):
        'symbol : SYMBOL'
        t[0] = SymbolEval(t[1])

    def p_literal(t):
        '''literal : TICK literal_expr
                   | NUMBER
                   | STRING'''
        if len(t) == 3:
            t[0] = LiteralEval(t[2])
        else:
            t[0] = LiteralEval(t[1])

    def p_literal_expr(t):
        '''literal_expr : SYMBOL
                        | literal_list'''
        t[0] = LiteralEval(t[1])

    def p_literal_list(t):
        'literal_list : LPAREN literal_exprs RPAREN'
        t[0] = LiteralEval(t[2])

    def p_literal_exprs(t):
        '''literal_exprs : literal_expr literal_exprs
                         | literal_expr'''
        if len(t) == 3:
            t[0] = LiteralEval([t[1]] + t[2].value())
        else:
            t[0] = LiteralEval([t[1]])

    return yacc.yacc()
