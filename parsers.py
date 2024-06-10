import ply.yacc as yacc
from lexer import tokens

variables = {}

def p_statement_for(p):
    '''statement : FOR LPAREN declaration SEMICOLON condition SEMICOLON increment RPAREN block'''
    p[0] = ('for', p[3], p[5], p[7], p[9])

def p_declaration(p):
    '''declaration : INT IDENTIFIER ASSIGN NUMBER'''
    if p[2] in variables:
        raise Exception(f"Variable '{p[2]}' already declared")
    variables[p[2]] = 'int'
    p[0] = ('declaration', p[2], p[4])

def p_condition(p):
    '''condition : IDENTIFIER LE NUMBER'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' not declared")
    if variables[p[1]] != 'int':
        raise Exception(f"Variable '{p[1]}' is not of type 'int'")
    p[0] = ('condition', p[1], p[3])

def p_increment(p):
    '''increment : IDENTIFIER INCREMENT'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' not declared")
    if variables[p[1]] != 'int':
        raise Exception(f"Variable '{p[1]}' is not of type 'int'")
    p[0] = ('increment', p[1])

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = ('block', p[2])

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_statement_println(p):
    '''statement : PRINTLN LPAREN STRING RPAREN SEMICOLON'''
    p[0] = ('println', p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parsers = yacc.yacc()
