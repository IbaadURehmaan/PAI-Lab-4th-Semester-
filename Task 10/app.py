from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simple dictionary storing our chatbot's knowledge about the Gold Campus
bot_knowledge = {
    "hello": "Hi! Welcome to the Superior University Gold Campus Admission Bot. How can I help?",
    "hi": "Hello! Ask me about our programs, deadlines, or admission requirements.",
    "programs": "At the Gold Campus, we offer BSAIM, BSCS, Software Engineering, and BBA.",
    "bsaim": "The BSAIM (BS Artificial Intelligence and Machine Learning) is a 4-year degree. It's a great choice!",
    "requirements": "You need a minimum of 50% marks in your Intermediate (FSC/ICS/FA) and you must pass our entry test.",
    "deadline": "The deadline for the Fall 2026 intake is August 15, 2026. Don't be late!",
    "fee": "Fee structures vary. Please visit the Gold Campus admission office in Lahore for exact details.",
    "location": "We are located at the Superior University Gold Campus in Lahore, Pakistan."
}

def generate_reply(user_text):
    # Convert user input to lowercase to make matching easier
    text_lower = user_text.lower()
    
    # Basic keyword matching loop
    for keyword in bot_knowledge:
        if keyword in text_lower:
            return bot_knowledge[keyword]
            
    # Default reply if the bot doesn't understand
    return "I am just a simple bot. Please ask me about 'programs', 'requirements', or 'deadlines'."

@app.route('/')
def home_page():
    # Loads the frontend HTML
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def chat():
    # Gets the message sent from the HTML form
    user_message = request.form['message']
    
    # Gets the bot's reply
    reply = generate_reply(user_message)
    
    # Sends the reply back to the HTML page
    return jsonify({"response": reply})

if __name__ == '__main__':
    app.run(debug=True)