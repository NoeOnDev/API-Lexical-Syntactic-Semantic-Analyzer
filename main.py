import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from lexer import analyze_code

load_dotenv()

app = Flask(__name__)

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5000))
origins = os.getenv('ORIGINS', '*')

CORS(app, resources={r"/*": {"origins": origins}})

@app.route('/analyze', methods=['POST'])
def analyze():
    code = request.json.get('code', '')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    tokens = analyze_code(code)
    return jsonify(tokens)

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
