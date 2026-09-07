@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running', 'message': 'Cyber Core AI Backend Active'}), 200
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_prompt = data.get('prompt', '')

        if not user_prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-chatbot-0zyn.onrender.com",
            "X-Title": "Cyber Core AI Bot"
        }

        payload = {
            "model": "liquid/lfm-2.5-2.6b:free",
            "messages": [
                {"role": "user", "content": user_prompt}
            ],
            "timeout": 45
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=45
        )

        res_data = response.json()

        if "choices" in res_data and len(res_data["choices"]) > 0:
            bot_reply = res_data["choices"][0]["message"]["content"]
            return jsonify({'reply': bot_reply})
        else:
            return jsonify({'error': 'OpenRouter Error', 'details': res_data}), 500

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Liquid model took too long to process (Render Timeout). Try a faster model like google/gemma-2-9b-it:free.'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
