import ply.lex as lex

reserved = {
    'setq': 'SETQ',
    'if': 'IF',
    'cond': 'COND',
    'defun': 'DEFUN',
    'let': 'LET',
    'prog': 'PROGN',
    'when': 'WHEN',
    'unless': 'UNLESS',
    'with': 'WITH',
    'self': 'SELF',
    }

tokens = [
    'SYMBOL',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'TICK',
    'STRING',
    ] + list(reserved.values())

def lexer():
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_TICK = r'\''

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_SYMBOL(t):
        r'[-+*/!@%^&=.a-zA-Z0-9_]+'
        t.value = t.value.lower()
        t.type = reserved.get(t.value, 'SYMBOL')
        return t

    def t_STRING(t):
        r'"([^"]|\")*?"'
        t.value = eval(t.value)
        return t

    def t_COMMENT(t):
        r';.*'
        pass

    t_ignore = ' \t\n'

    def t_error(t):
        print(('Illegal character: %s' % t.value[0]))
        t.lexer.skip(1)

    lexer = lex.lex()

    return lexer
