from flask import Flask, request, jsonify
from flask_cors import CORS
from lexer import lexer
from parsers import parsers, variables, initialized_variables

app = Flask(__name__)
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze_code():
    code = request.json.get('code')

    if not isinstance(code, str):
        return jsonify({'error': 'Invalid code'}), 400

    lexer.input(code)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: 
            break
        tokens.append({'type': tok.type, 'value': tok.value, 'line': tok.lineno})

    try:
        variables.clear()
        initialized_variables.clear()
        parse_result = parsers.parse(code)
        message = 'El ciclo for cumple con las reglas y estructura' if 'for' in parse_result else 'No se encontró un ciclo for'
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'lexical_analysis': tokens,
        'parse_result': parse_result,
        'message': message
    })


if __name__ == '__main__':
    app.run(debug=True)
