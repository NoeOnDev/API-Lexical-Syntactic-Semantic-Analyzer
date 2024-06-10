from flask import Flask, request, jsonify
from lexer import lexer
from parsers import parsers, variables, initialized_variables

app = Flask(__name__)

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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'lexical_analysis': tokens,
        'parse_result': parse_result
    })


if __name__ == '__main__':
    app.run(debug=True)
