from flask import Flask, render_template, request
import openai
import time

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "YOUR_API"

def generate_response(prompt):
    try:
        # Use the OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300,  # Increased max_tokens for longer responses
            n=1,
            stop=None
        )

        # Extract and return the generated text from the API response
        return response.choices[0].text.strip()
    except openai.error.RateLimitError as e:
        # Handle rate limit error by waiting for a minute (you can adjust this)
        print(f"Rate limit exceeded. Waiting for a minute. Error: {e}")
        time.sleep(60)
        return generate_response(prompt)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    chat_history = request.form['chat_history']

    # Check if the current user input is the same as the previous one
    if chat_history.endswith(f"\nUser: {user_input}\nAI:"):
        # If it's the same, return the previous response
        ai_response = chat_history.split('\n')[-1].split(':')[-1].strip()
    else:
        # Combine user input and chat history
        prompt = f"{chat_history}\nUser: {user_input}\nAI:"

        # Generate AI response
        ai_response = generate_response(prompt)

        # Update chat history
        chat_history += f"\nUser: {user_input}\nAI: {ai_response}"

    return {'ai_response': ai_response, 'chat_history': chat_history}

if __name__ == '__main__':
    app.run(debug=True)
