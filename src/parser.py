import lexer as lxr
from lexer import tokens
import ply.yacc as yacc
import symbol

def parser():
  def p_sexpseq(t):
    'sexpseq : sexps'
    t[0] = t[1]

  def p_sexps(t):
    '''sexps : sexps sexp
             | sexp'''
    if len(t) == 3:
      t[0] = t[1] + [t[2]]
    else:
      t[0] = [t[1]]

  def p_sexp(t):
    'sexp : LPAREN exp_list RPAREN'
    t[0] = tuple(t[2])

  def p_exp_list(t):
    '''exp_list : exp exp_list
                | exp'''
    if len(t) == 3:
      t[0] = [t[1]] + t[2]
    else:
      t[0] = [t[1]]

  def p_exp(t):
    '''exp : atom
           | sexp
           | list'''
    t[0] = t[1]

  def p_list(t):
    'list : LSQUARE exp_list RSQUARE'
    t[0] = t[2]

  def p_atom(t):
    '''atom : NUMBER
            | symbol
            | STRING'''
    t[0] = t[1]

  def p_symbol(t):
    'symbol : SYMBOL'
    t[0] = symbol.symbol(t[1])

  def p_error(t):
    print("Error before token %s." % yacc.token())

  # required by PLY, unfortunately
  lexer = lxr.lexer()
  return yacc.yacc()
