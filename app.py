import openai
from flask import Flask, request, jsonify, render_template_string

# Initialize a Flask application
app = Flask(__name__)

# Set the API key for OpenAI
openai.api_key = "sk-proj-Y86w6mZD8lzmOMoJCYHtT3BlbkFJ1QJhIO7rF2doVhqdkJSU"

@app.route("/")
def home():
    # Serve the HTML file when accessing the root URL
    # This function reads the 'index.html' file and sends it to the client as an HTML response
    return render_template_string(open("index.html").read())

@app.route("/chat", methods=["POST"])
def chat():
    # Route to handle chat messages via POST requests
    # Extracts 'message' from the JSON payload of the request
    user_input = request.json["message"]
    # Get the response from the GPT model based on the user input
    response = chat_with_gpt(user_input)
    # Return the model's response as a JSON object
    return jsonify({'answer': response})

def chat_with_gpt(prompt):
    # Function to handle interaction with OpenAI's GPT model
    # Prepare the messages list with user's input and a fixed assistant's introduction
    messages = [
        {"role": "user", "content": prompt},  # User's message
        {"role": "assistant", "content": "My name is Clara and I'm here to assist you with managing your online screen and answer any questions you may have regarding your mental health as a result of your screentime"}
    ]
    # Call to OpenAI API to get a response based on the conversation history
    response_data = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    # Extract the message content and strip any leading/trailing whitespace
    response = response_data['choices'][0]['message']['content'].strip()
    return response

if __name__ == "__main__":
    # Runs the Flask application only if this script is executed as the main program
    app.run(debug=True)  # Enables debug mode which provides detailed error logs and live reloading