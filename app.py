from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Direct ChatOpenAI wrapper use kar standard OpenRouter headers ke saath
model = ChatOpenAI(
    model="meta-llama/llama-3.3-70b-instruct:free",  # Working free model on OpenRouter
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={
        "HTTP-Referer": "https://render.com",
        "X-Title": "NEIGHBOUR-CORE"
    }
)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_question = data.get("prompt", "")
        
        if not user_question:
            return jsonify({"error": "Prompt is required"}), 400

        messages = [
            SystemMessage(content="You are a helpful AI assistant."),
            HumanMessage(content=user_question)
        ]
        
        response = model.invoke(messages)

        return jsonify({"reply": response.content}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
