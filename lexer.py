import ply.lex as lex

tokens = (
    'FOR', 'INT', 'IDENTIFIER', 'NUMBER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'LE', 'PRINTLN', 'STRING', 'ASSIGN', 'PLUS', 'INCREMENT',
    'DIV', 'MINUS', 'TIMES'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_LE = r'<='
t_ASSIGN = r'='
t_PLUS = r'\+'
t_INCREMENT = r'\+\+'
t_DIV = r'/'
t_MINUS = r'-'
t_TIMES = r'\*'

t_ignore = ' \t'

def t_FOR(t):
    r'for'
    t.type = 'FOR'
    return t

def t_INT(t):
    r'int'
    t.type = 'INT'
    return t

def t_PRINTLN(t):
    r'System\.out\.println'
    t.type = 'PRINTLN'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'IDENTIFIER'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    t.type = 'NUMBER'
    return t

def t_STRING(t):
    r'\".*?\"'
    t.type = 'STRING'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
