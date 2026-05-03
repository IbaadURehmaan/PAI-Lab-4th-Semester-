from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    # URL for a free public joke API
    api_url = "https://official-joke-api.appspot.com/random_joke"
    
    try:
        # Fetching data from the free API
        response = requests.get(api_url)
        joke_data = response.json()
        
        # Extracting the setup and punchline from the JSON response
        joke_setup = joke_data['setup']
        joke_punchline = joke_data['punchline']
        
    except:
        # Simple error handling just in case the internet is down
        joke_setup = "Oops! Could not connect to the API."
        joke_punchline = "Please check your internet and try again."

    # Sending the variables to the HTML page
    return render_template('index.html', setup=joke_setup, punchline=joke_punchline)

if __name__ == '__main__':
    # Running the Flask app
    app.run(debug=True)