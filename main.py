from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
import ply.lex as lex
import ply.yacc as yacc

load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
ORIGINS = os.getenv('ORIGINS')

app = Flask(__name__)
CORS(app, origins=ORIGINS)

tokens = (
    'PR', 'ID', 'PI', 'PD', 'LI', 'LD', 'PC', 'NUM', 'OP', 'CO', 'DOT', 'STRING'
)

reserved = {
    'int': 'PR',
    'for': 'PR'
}

t_PI = r'\('
t_PD = r'\)'
t_LI = r'\{'
t_LD = r'\}'
t_PC = r';'
t_OP = r'\+|-|\*|<=|='
t_CO = r','
t_DOT = r'\.'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def analyze_content(content):
    lexer.lineno = 1
    lexer.input(content)
    result = []
    for tok in lexer:
        result.append({"id": str(uuid.uuid4()), "linea": tok.lineno, "type": tok.type, "value": tok.value, "token": tok.value})
    return result

def p_for_loop(p):
    '''for_loop : PR PI declaration PC condition PC increment PD LI statement LD'''
    p[0] = "Valid 'for' loop"

def p_declaration(p):
    '''declaration : PR ID OP NUM
                   | ID OP NUM'''
    pass

def p_condition(p):
    '''condition : ID OP NUM'''
    pass

def p_increment(p):
    '''increment : ID OP ID'''
    pass

def p_statement(p):
    '''statement : ID DOT ID DOT ID PI STRING PD PC'''
    if p[1] != "system" or p[3] != "out" or p[5] != "println":
        print(f"Error en la línea {p.lineno(1)}: 'system.out.println' incorrecto.")
        raise SyntaxError

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def analyze_syntax(content):
    try:
        parser.parse(content, lexer=lexer)
        return {"status": "success", "message": "Valid 'for' loop"}
    except SyntaxError:
        return {"status": "error", "message": "Invalid 'for' loop"}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_response(jsonify({"error": "No file part"}), 400)
    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({"error": "No selected file"}), 400)
    if file:
        content = file.read().decode('utf-8')
        lex_result = analyze_content(content)
        syntax_result = analyze_syntax(content)
        return jsonify({"lexical_analysis": lex_result, "syntax_analysis": syntax_result})

@app.route('/analyze', methods=['POST'])
def analyze_code():
    code = request.data.decode('utf-8')
    if not isinstance(code, str):
        return make_response(jsonify({"error": "Invalid input"}), 400)
    lex_result = analyze_content(code)
    syntax_result = analyze_syntax(code)
    return jsonify({"lexical_analysis": lex_result, "syntax_analysis": syntax_result})

@app.route('/')
def hello_world():
    return 'Hello, World! Api-back-end is running on {}:{}'.format(HOST, PORT)

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
