import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

host = os.getenv('HOST', '0.0.0.0')
port = int(os.getenv('PORT', 5000))
origins = os.getenv('ORIGINS', '*')

CORS(app, resources={r"/*": {"origins": origins}})

if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
