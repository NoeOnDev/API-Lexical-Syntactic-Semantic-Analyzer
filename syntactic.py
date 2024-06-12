import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    '''program : FOR LPAREN declaration SEMICOLON condition SEMICOLON iteration RPAREN block'''
    p[0] = ('for_loop', p[3], p[5], p[7], p[9])

def p_declaration(p):
    '''declaration : INT ID EQ NUMBER'''
    p[0] = ('declaration', p[1], p[2], p[4])

def p_condition(p):
    '''condition : ID LE NUMBER'''
    p[0] = ('condition', p[1], p[2], p[3])

def p_iteration(p):
    '''iteration : ID PLUS PLUS'''
    p[0] = ('iteration', p[1], '++')

def p_block(p):
    '''block : LBRACE statement RBRACE'''
    p[0] = ('block', p[2])

def p_statement(p):
    '''statement : PRINTLN LPAREN STRING RPAREN SEMICOLON'''
    p[0] = ('statement', p[1], p[3])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

def parse_code(code):
    return parser.parse(code)
