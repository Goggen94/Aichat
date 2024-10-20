from flask import Flask, jsonify, request, render_template
import openai
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Set your OpenAI API key
openai.api_key = "sk-DjqztWy3uvhY8Wdgq567xeanC4zhTM-zFF5DF-WKDYT3BlbkFJoEPMmNIVix54I8-sKQWPT-AEu_O9Z2SUs_zr899gsA"  # Replace with your actual OpenAI API key

@app.route("/", methods=["GET"])
def index():
    return render_template('chat.html')  # Render chat.html

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "No message received."}), 400
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can change this to your preferred model
            prompt=user_message,
            max_tokens=150
        )
        ai_response = response['choices'][0]['text'].strip()
        return jsonify({"response": ai_response})
    except Exception as e:
        logging.error(f"Error with AI response: {e}")
        return jsonify({"response": "There was an error with the AI service."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
