import os
from openai import OpenAI
from flask import Flask, request, render_template, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

context = "You are an AI trained to provide career counseling advice. "

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = context + request.form['message']

    # Placeholder for your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")

    # Setting up the headers for the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # ChatGPT API endpoint
    url = "https://api.openai.com/v1/chat/completions"

    # Preparing the data for the POST request
    data = {
        'model': 'gpt-3.5-turbo',
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7,
        "max_tokens": 150  # Adjust the number of tokens as needed
    }

    # Sending the request to the ChatGPT API
    response = requests.post(url, headers=headers, json=data)
    # Checking if the request was successful
    if response.status_code == 200:
        # Extracting the text from the response
        chat_response = response.json().get("choices", [{}])[0].get("message", "").get("content", "").strip()
        # chat_response = response.json()['choices'][0]['message']['content']
        return ({"message": chat_response})
        # return jsonify({"message": chat_response})
    else:
        # In case of an error, return an appropriate message
        return jsonify({"error": "Failed to fetch response from the API"})

if __name__ == '__main__':
    app.run(debug=True)
