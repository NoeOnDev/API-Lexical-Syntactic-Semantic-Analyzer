import ply.lex as lex

tokens = (
    'FOR', 'LPAREN', 'RPAREN', 'SEMICOLON', 'INT', 'ID', 'EQ', 'LE', 'PLUS', 'LBRACE', 'RBRACE', 'PRINTLN', 'DOT', 'NUMBER', 'STRING'
)

reserved = {
    'for': 'FOR',
    'int': 'INT',
    'System.out.println': 'PRINTLN'
}

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_EQ = r'='
t_LE = r'<='
t_PLUS = r'\+'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_STRING = r'\".*?\"'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_code(code):
    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append((tok.type, tok.value))
    return tokens
