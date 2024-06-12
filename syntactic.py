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
    if p:
        error_message = f"Syntax error at '{p.value}'"
        error_position = {'line': p.lineno, 'position': p.lexpos}
        raise SyntaxError(error_message, error_position)
    else:
        error_message = "Syntax error at EOF"
        raise SyntaxError(error_message, None)

parser = yacc.yacc()

def parse_code(code):
    try:
        result = parser.parse(code)
        return {'result': result, 'message': "El ciclo for cumple con la estructura", 'error': None}
    except SyntaxError as e:
        error_message, error_position = e.args
        return {'result': None, 'message': error_message, 'error': error_position}
    except Exception as e:
        return {'result': None, 'message': str(e), 'error': None}
