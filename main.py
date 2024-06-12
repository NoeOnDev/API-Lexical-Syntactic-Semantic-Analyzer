import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from lexer import analyze_code
from syntactic import parse_code
from semantic import analyze_semantics

load_dotenv()

app = Flask(__name__)

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5000))
origins = os.getenv('ORIGINS', '*')

CORS(app, resources={r"/*": {"origins": origins}})

@app.route('/analyze_lexical', methods=['POST'])
def analyze_lexical():
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No se proporcionó código'}), 400
    tokens = analyze_code(code)
    return jsonify(tokens)

@app.route('/analyze_syntactic', methods=['POST'])
def analyze_syntactic():
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No se proporcionó código'}), 400
    result = parse_code(code)
    return jsonify(result)

@app.route('/analyze_semantic', methods=['POST'])
def analyze_semantic():
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No se proporcionó código'}), 400
    
    tokens = analyze_code(code)
    if 'error' in tokens:
        return jsonify(tokens)
    
    parsed_code = parse_code(code)
    if 'error' in parsed_code:
        return jsonify(parsed_code)
    
    semantic_result = analyze_semantics(parsed_code)
    return jsonify(semantic_result)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
