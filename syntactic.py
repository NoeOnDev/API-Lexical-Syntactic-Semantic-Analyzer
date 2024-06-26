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
    '''statement : SYSOUT LPAREN expression RPAREN SEMICOLON
                 | declaration SEMICOLON
                 | assignment SEMICOLON
                 | for_loop'''
    p[0] = ('statement', p[1])

def p_declaration(p):
    '''declaration : INT ID ASSIGN expression'''
    p[0] = ('declaration', p[2], p[4])

def p_assignment(p):
    '''assignment : ID ASSIGN expression
                  | ID INCREMENT'''
    if len(p) == 4:
        p[0] = ('assignment', p[1], p[3])
    else:
        p[0] = ('increment', p[1])

def p_for_loop(p):
    '''for_loop : FOR LPAREN declaration SEMICOLON expression SEMICOLON assignment RPAREN block'''
    p[0] = ('for_loop', p[3], p[5], p[7], p[9])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term
                  | expression TIMES term
                  | expression DIVIDE term
                  | expression EQUALS term
                  | expression LE term
                  | expression LT term
                  | expression GE term
                  | expression GT term'''
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
        return {"success": "El análisis de sintaxis se completó correctamente. La estructura del programa es correcta.", "result": result}
