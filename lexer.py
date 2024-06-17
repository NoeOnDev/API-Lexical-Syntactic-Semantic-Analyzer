import ply.lex as lex

tokens = (
    'INICIO', 'CADENA', 'ENTERO', 'VAR', 'NUM', 'PROCESO', 'SI', 'IGUAL', 'IGUAL_IGUAL', 'FIN', 'PUNTOYCOMA', 'LLAVE_ABRIR', 'LLAVE_CERRAR', 'LPAREN', 'RPAREN', 'STRING',
)

reserved = {
    'inicio': 'INICIO',
    'cadena': 'CADENA',
    'entero': 'ENTERO',
    'proceso': 'PROCESO',
    'si': 'SI',
    'fin': 'FIN',
}

t_IGUAL = r'='
t_IGUAL_IGUAL = r'=='
t_PUNTOYCOMA = r';'
t_LLAVE_ABRIR = r'\{'
t_LLAVE_CERRAR = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'VAR')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en línea {t.lineno}, posición {t.lexpos}")
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