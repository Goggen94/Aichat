from flask import Flask, jsonify, request, render_template
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Fetch the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/", methods=["GET"])
def index():
    return render_template('chat.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"response": "No message received."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({"response": "There was an error with the AI service."}), 500

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
