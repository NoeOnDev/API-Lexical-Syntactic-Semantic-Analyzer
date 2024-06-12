import ply.yacc as yacc
from lexer import tokens

error_message = None

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
    global error_message
    if p is None:
        error_message = "Error de sintaxis en EOF"
    else:
        error_message = f"Error de sintaxis en '{p.value}'"

parser = yacc.yacc()

def parse_code(code):
    global error_message
    result = parser.parse(code)
    if result is None:
        return {"error": error_message}
    else:
        return {"success": "El análisis sintáctico se completó con éxito. La estructura del ciclo 'for' es correcta.", "result": result}
