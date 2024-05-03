import openai
from flask import Flask, request, jsonify, render_template_string,session
from flask_session import Session

# Initialize a Flask application
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Use file-based session
Session(app)
# Set the API key for OpenAI
openai.api_key = "API KEY GOES HERE"

@app.route("/")
def home():
    # Serve the HTML file when accessing the root URL
    # This function reads the 'index.html' file and sends it to the client as an HTML response
    return render_template_string(open("index.html").read())

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    if 'chat_history' not in session:
        session['chat_history'] = []  # Initialize chat history if not already present
    # Append the new user message to the session history
    session['chat_history'].append({"role": "user", "content": user_input})
    response = chat_with_gpt(session['chat_history'])
    session['chat_history'].append({"role": "assistant", "content": response})
    return jsonify({'answer': response})

def chat_with_gpt(messages):
    # Call to OpenAI API to get a response based on the conversation history
    response_data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    response = response_data['choices'][0]['message']['content'].strip()
    return response

if __name__ == "__main__":
    app.run(debug=True)