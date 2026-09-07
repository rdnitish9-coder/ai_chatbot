from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

model = init_chat_model(
    model="liquid/lfm-2.5-2.6b:free",
    model_provider="openai",
    openai_api_base="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_question = data.get("prompt", "")
        
        if not user_question:
            return jsonify({"error": "Prompt is required"}), 400

        # System prompt + Dynamic User question list
        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content=user_question)
        ]
        
        # Model invoke
        response = model.invoke(messages)

        return jsonify({"reply": response.content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
