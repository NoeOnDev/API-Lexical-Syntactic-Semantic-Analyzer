import ply.lex as lex

tokens = (
    'FOR', 'INT', 'IDENTIFIER', 'NUMBER', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'LE', 'PRINTLN', 'STRING', 'ASSIGN', 'PLUS', 'INCREMENT'
)

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_SEMICOLON = r';'
t_LE = r'<='
t_ASSIGN = r'='
t_PLUS = r'\+'
t_INCREMENT = r'\+\+'

t_ignore = ' \t'

def t_FOR(t):
    r'for'
    return t

def t_INT(t):
    r'int'
    return t

def t_PRINTLN(t):
    r'System\.out\.println'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'\".*?\"'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
