from flask import Flask, render_template, request
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get environment variables
MARKETSTACK_API_KEY = os.getenv('Market_API_Key')
BASE_URL = os.getenv('Base_URL')

@app.route('/')
def index():
    stock_symbol = request.args.get('symbol', 'AAPL')  # Default to Apple stock (AAPL)
    url = f"{BASE_URL}?access_key={MARKETSTACK_API_KEY}&symbols={stock_symbol}"
    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        stock_data = data['data'][0]
        return render_template('index.html', stock_data=stock_data)
    else:
        return f"Error: {data.get('error', {}).get('message', 'Unable to fetch data')}"

if __name__ == '__main__':
    app.run(debug=True)
