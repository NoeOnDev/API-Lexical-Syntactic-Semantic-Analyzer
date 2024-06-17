import ply.yacc as yacc
from lexer import tokens

error_message = None

def p_program(p):
    '''program : INICIO PUNTOYCOMA declarations PROCESO PUNTOYCOMA statements FIN PUNTOYCOMA'''
    p[0] = ('program', p[3], p[6])

def p_declarations(p):
    '''declarations : declaration declarations
                    | declaration'''
    if len(p) == 3:
        p[0] = ('declarations', p[1], p[2])
    else:
        p[0] = ('declarations', p[1])

def p_declaration(p):
    '''declaration : CADENA VAR IGUAL STRING PUNTOYCOMA
                   | ENTERO VAR IGUAL NUM PUNTOYCOMA'''
    p[0] = ('declaration', p[2], p[4])

def p_statements(p):
    '''statements : statement statements
                  | statement'''
    if len(p) == 3:
        p[0] = ('statements', p[1], p[2])
    else:
        p[0] = ('statements', p[1])

def p_statement(p):
    '''statement : SI LPAREN condition RPAREN block
                 | assignment'''
    if len(p) == 6:
        p[0] = ('statement', 'if', p[3], p[5])
    else:
        p[0] = p[1]

def p_condition(p):
    '''condition : VAR IGUAL_IGUAL NUM
                 | VAR IGUAL_IGUAL STRING'''
    p[0] = ('condition', p[1], p[3])

def p_block(p):
    '''block : LLAVE_ABRIR statements LLAVE_CERRAR'''
    p[0] = ('block', p[2])

def p_assignment(p):
    '''assignment : VAR IGUAL STRING PUNTOYCOMA
                  | VAR IGUAL NUM PUNTOYCOMA'''
    p[0] = ('assignment', p[1], p[3])

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
        return {"success": "El análisis sintáctico se completó con éxito. La estructura del programa es correcta.", "result": result}