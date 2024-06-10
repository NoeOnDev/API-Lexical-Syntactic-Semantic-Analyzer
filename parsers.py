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
        raise Exception(f"Variable '{p[2]}' ya declarada")
    variables[p[2]] = 'int'
    initialized_variables.add(p[2])
    p[0] = ('declaration', p[2], p[4])

def p_condition(p):
    '''condition : IDENTIFIER LE NUMBER'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' no declarada")
    if p[1] not in initialized_variables:
        raise Exception(f"Variable '{p[1]}' no inicializada")
    if variables[p[1]] != 'int':
        raise Exception(f"Variable '{p[1]}' no es de tipo 'int'")
    p[0] = ('condition', p[1], p[3])

def p_increment(p):
    '''increment : IDENTIFIER INCREMENT'''
    if p[1] not in variables:
        raise Exception(f"Variable '{p[1]}' no declarada")
    if p[1] not in initialized_variables:
        raise Exception(f"Variable '{p[1]}' no inicializada")
    if variables[p[1]] != 'int':
        raise Exception(f"Variable '{p[1]}' no es de tipo 'int'")
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
        raise Exception(f"Variable '{p[1]}' no declarada")
    if variables[p[1]] != 'int' or not isinstance(p[3], int):
        raise Exception(f"Error de tipo en la asignación a '{p[1]}'")
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
        raise Exception("Error de tipo en la suma")
    p[0] = p[1] + p[3]

def p_expression_sub(p):
    '''expression : expression MINUS expression'''
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Error de tipo en la resta")
    p[0] = p[1] - p[3]

def p_expression_mul(p):
    '''expression : expression TIMES expression'''
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Error de tipo en la multiplicación")
    p[0] = p[1] * p[3]

def p_expression_div(p):
    '''expression : expression DIV expression'''
    if p[3] == 0:
        raise Exception("División por cero")
    if not (isinstance(p[1], int) and isinstance(p[3], int)):
        raise Exception("Error de tipo en la división")
    p[0] = p[1] / p[3]

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
    else:
        print("Error de sintaxis al final del archivo")

parsers = yacc.yacc()
