import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_URL = os.getenv('API_URL', 'http://localhost:8000/api/agent')
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '30'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        question = data.get('question', '')
        user = data.get('user', 'anonymous')
        
        if not question:
            return jsonify({
                'error': 'Question is required'
            }), 400
        
        # Call the API
        payload = {
            'question': question,
            'user': user
        }
        
        response = requests.post(
            API_URL,
            json=payload,
            timeout=API_TIMEOUT
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({
                'error': f'API error: {response.status_code}',
                'details': response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Request timeout',
            'details': 'The API took too long to respond'
        }), 504
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Connection error',
            'details': 'Could not connect to the API'
        }), 503
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
