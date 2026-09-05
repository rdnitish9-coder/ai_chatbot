from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
import os

app = Flask(__name__)
CORS(app)  # Isse browser frontend request block nahi karega

model = init_chat_model(
    model ="liquid/lfm-2.5-2.6b:free",
    model_provider = "openai",
    openai_api_base = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENROUTER_API_KEY")
)

@app.route('/api/chat', methods=['POST'])
def chat():
    # 1. Frontend se text/query receive kar
    data = request.get_json()
    user_msg = data.get('prompt', '')

    # 2. Tera Python Logic / ML Model yahan kaam karega
    # (Abhi ke liye test response de rahe hain)
    ai_response = model.invoke(user_msg).content
    return jsonify({'reply': ai_response})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS

# Tera existing LLM / Model import yahan aayega
# Example: from langchain_community.chat_models import ...
# ya import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Cross-Origin support for Web UI


def generate_ai_response(user_query):
    # -------------------------------------------------------------
    # YAHAN TERA VO CODE AAYEGA JO TERMINAL ME AI RESPONSE DETAH THA
    # -------------------------------------------------------------
    # Example dummy placeholder (apne real model call se replace kar lena):
    # response = model.generate_content(user_query)
    # return response.text

    # Example logic matching your terminal code:
    ai_text = f"Hello! 👋 How can I help you today?"  # Tera actual AI model function response yahan se return hoga
    return ai_text


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('prompt', '')

    if not user_msg:
        return jsonify({'reply': 'Empty prompt received.'}), 400

    # Model ko call kar
    ai_reply = generate_ai_response(user_msg)

    # UI ko exact AI ka response bhej
    return jsonify({'reply': ai_reply})


if __name__ == '__main__':
    print("[CYBER_BACKEND] AI Model Server Running on http://127.0.0.1:5000")
    app.run(port=5000, debug=True)