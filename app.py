from flask import Flask, jsonify, request, render_template
import openai
import logging
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('KEYKEY')

@app.route("/", methods=["GET"])
def index():
    return render_template('chat.html')  # Render chat.html from templates

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        app.logger.error("No message received.")
        return jsonify({"response": "No message received."}), 400
    
    app.logger.info(f"Message received: {user_message}")
    
    # Send the user's message to the OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        app.logger.error(f"Error fetching AI response: {e}")
        return jsonify({"response": "There was an error with the AI service."}), 500
    
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
