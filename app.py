from flask import Flask, render_template
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

app = Flask(__name__)

def getprice():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    par = {
        'slug' : 'bitcoin',
        'convert' : 'USD'
    }
    headers = {
        'Accepts' : 'application/json',
        'X-CMC_PRO_API_KEY': 'b6f132c6-9422-4347-8311-8debe96a3855',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=par)
        data = json.loads(response.text)
        coin_price = data['data']['1']['quote']['USD']['price']
        return coin_price
        # pprint.pprint(data['data']['1']['quote']['USD']['price'])
        #f = open('myjson.json', 'w')
        #f.write(json.dumps((data)))
        #f.close()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

@app.route('/')
def home():
    price = getprice()  # Get the Bitcoin price
    return render_template('index.html', price=price)

@app.route('/get_bitcoin_price')
def get_price():
    price = getprice()  # Call the renamed function to get the updated Bitcoin price
    return json.dumps({'price': price})  # Return the price as JSON

if __name__ == '__main__':
    app.run(debug=True)