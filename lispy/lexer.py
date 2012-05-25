import ply.lex as lex

tokens = [
    'LPAREN', 'LSQUARE', 'NUMBER', 'RPAREN',
    'RSQUARE', 'STRING', 'SYMBOL', 'TICK',
    ]

def lexer():
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_TICK = r'\''
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_SYMBOL(t):
        r'[-+*/!@%^&=.a-zA-Z0-9_]+'
        t.value = t.value.lower()
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
