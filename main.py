from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
import ply.lex as lex
import re

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
    'for': 'PR',
    'public': 'PR',
    'class': 'PR',
    'static': 'PR',
    'void': 'PR',
    'String': 'PR',
    'System': 'PR',
    'out': 'PR',
    'println': 'PR'
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

def validar_hola_mundo(codigo):
    patron_clase = re.compile(r'public\s+class\s+\w+\s*\{')
    patron_main = re.compile(r'public\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s*[a-zA-Z]+\s*\)\s*\{')
    patron_print = re.compile(r'System\.out\.println\s*\(\s*\"Hola Mundo!\"\s*\)\s*;')
    lineas = codigo.split('\n')
    
    if len(lineas) < 5:
        return False, "Código incompleto", None, None
    
    if not patron_clase.match(lineas[0].strip()):
        error_pos = patron_clase.search(lineas[0])
        return False, "Error en la sintaxis de la declaración de clase", 0, error_pos.start() if error_pos else None
    
    if not patron_main.match(lineas[1].strip()):
        error_pos = patron_main.search(lineas[1])
        return False, "Error en la sintaxis de la declaración del método main", 1, error_pos.start() if error_pos else None
    
    if not patron_print.match(lineas[2].strip()):
        error_pos = patron_print.search(lineas[2])
        return False, "Error en la sintaxis de System.out.println", 2, error_pos.start() if error_pos else None
    
    if lineas[3].strip() != '}' or lineas[4].strip() != '}':
        return False, "Falta el cierre del bloque", 3 if lineas[3].strip() != '}' else 4, len(lineas[3]) if lineas[3].strip() != '}' else len(lineas[4])
    
    return True, "El programa Hola Mundo es correcto", None, None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return make_response(jsonify({"error": "No file part"}), 400)
    file = request.files['file']
    if file.filename == '':
        return make_response(jsonify({"error": "No selected file"}), 400)
    if file:
        content = file.read().decode('utf-8')
        lexical_result = analyze_content(content)
        valido, mensaje, linea_error, posicion_error = validar_hola_mundo(content)
        response = {
            "lexical_analysis": lexical_result,
            "validation": {
                "valid": valido,
                "message": mensaje,
                "line_error": linea_error,
                "position_error": posicion_error
            }
        }
        if not lexical_result:
            return make_response(jsonify({"error": "Not found tokens in the file"}), 404)
        return jsonify(response)

@app.route('/analyze', methods=['POST'])
def analyze_code():
    code = request.data.decode('utf-8')
    if not isinstance(code, str):
        return make_response(jsonify({"error": "Invalid input"}), 400)
    
    lexical_result = analyze_content(code)
    valido, mensaje, linea_error, posicion_error = validar_hola_mundo(code)
    response = {
        "lexical_analysis": lexical_result,
        "validation": {
            "valid": valido,
            "message": mensaje,
            "line_error": linea_error,
            "position_error": posicion_error
        }
    }
    
    return jsonify(response)

@app.route('/')
def hello_world():
    return 'Hello, World! Api-back-end is running on {}:{}'.format(HOST, PORT)

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
