import ply.yacc as yacc
from lexer import tokens

error_message = None

def p_program(p):
    '''program : PUBLIC CLASS ID LBRACE main_method RBRACE'''
    p[0] = ('program', p[3], p[5])

def p_main_method(p):
    '''main_method : PUBLIC STATIC VOID MAIN LPAREN STRING LBRACKET RBRACKET ID RPAREN block'''
    p[0] = ('main_method', p[11])

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = ('block', p[2])

def p_statements(p):
    '''statements : statement
                  | statement statements'''
    if len(p) == 2:
        p[0] = ('statements', p[1])
    else:
        p[0] = ('statements', p[1], p[2])

def p_statement(p):
    '''statement : SYSOUT LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('statement', p[3])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binary_op', p[2], p[1], p[3])

def p_term(p):
    '''term : TEXT
            | NUMBER
            | ID'''
    p[0] = ('term', p[1])

def p_error(p):
    global error_message
    if p is None:
        error_message = "Syntax error at EOF"
    else:
        error_message = f"Syntax error at '{p.value}'"

parser = yacc.yacc()

def parse_code(code):
    global error_message
    result = parser.parse(code)
    if result is None:
        return {"error": error_message}
    else:
        return {"success": "Syntax analysis completed successfully. The program structure is correct.", "result": result}
