import ply.lex as lex

tokens = (
    'PUBLIC', 'CLASS', 'STATIC', 'VOID', 'MAIN', 'STRING',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'SYSOUT',
    'ID', 'TEXT', 'LBRACKET', 'RBRACKET', 'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'
)

reserved = {
    'public': 'PUBLIC',
    'class': 'CLASS',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'String': 'STRING'
}

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_SYSOUT(t):
    r'System\.out\.println'
    return t

def t_TEXT(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.type = 'TEXT'
    return t

def t_NUMBER(t):
    r'\d+'
    t.type = 'NUMBER'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_code(code):
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value, tok.lineno, tok.lexpos))
    return tokens
