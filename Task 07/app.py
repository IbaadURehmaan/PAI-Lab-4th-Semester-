import requests
from flask import Flask, render_template, request

app = Flask(__name__)

def fetch_useless_fact():
    target_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"
    api_response = requests.get(target_url)
    
    if api_response.status_code == 200:
        return api_response.json()
    return None

@app.route('/', methods=['GET', 'POST'])
def main_dashboard():
    fact_data = None
    
    if request.method == 'POST':
        fact_data = fetch_useless_fact()
            
    return render_template('index.html', info=fact_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)