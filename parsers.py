import ply.yacc as yacc
from lexer import tokens

variables = {}
initialized_variables = set()

def p_statement_for(p):
    '''statement : FOR LPAREN declaration SEMICOLON condition SEMICOLON increment RPAREN block'''
    p[0] = ('for', p[3], p[5], p[7], p[9])

def p_declaration(p):
    '''declaration : INT IDENTIFIER ASSIGN NUMBER'''
    if p[2] in variables:
        raise Exception(f"Variable '{p[2]}' already declared")
    variables[p[2]] = 'int'
    initialized_variables.add(p[2])
    p[0] = ('declaration', p[2], p[4])

def p_condition(p):
    '''condition : IDENTIFIER LE NUMBER'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' not declared")
    if p[1] not in initialized_variables:
        raise Exception(f"Variable '{p[1]}' not initialized")
    if variables[p[1]] != 'int':
        raise Exception(f"Variable '{p[1]}' is not of type 'int'")
    p[0] = ('condition', p[1], p[3])

def p_increment(p):
    '''increment : IDENTIFIER INCREMENT'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' not declared")
    if p[1] not in initialized_variables:
        raise Exception(f"Variable '{p[1]}' not initialized")
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

def p_statement_assignment(p):
    '''statement : IDENTIFIER ASSIGN expression SEMICOLON'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' not declared")
    if variables[p[1]] != 'int' or not isinstance(p[3], int):
        raise Exception(f"Type mismatch in assignment to '{p[1]}'")
    initialized_variables.add(p[1])
    p[0] = ('assignment', p[1], p[3])

def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

def p_expression_string(p):
    '''expression : STRING'''
    p[0] = p[1]

def p_expression_add(p):
    '''expression : expression PLUS expression'''
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Type mismatch in addition")
    p[0] = p[1] + p[3]

def p_expression_sub(p):
    '''expression : expression MINUS expression'''
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Type mismatch in subtraction")
    p[0] = p[1] - p[3]

def p_expression_mul(p):
    '''expression : expression TIMES expression'''
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Type mismatch in multiplication")
    p[0] = p[1] * p[3]

def p_expression_div(p):
    '''expression : expression DIV expression'''
    if p[3] == 0:
        raise Exception("Division by zero")
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Type mismatch in division")
    p[0] = p[1] / p[3]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parsers = yacc.yacc()
