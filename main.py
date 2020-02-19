import sqlite3
from flask import Flask, request, g, redirect, url_for, render_template, abort, jsonify
from contextlib import closing
import json
import requests



# configuration

app = Flask(__name__)
app.config.from_object(__name__)


# keys

token = ''
account_id = ''
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token, 'accountID': account_id,}




# open trade: http://<public ip>/EUR_USD/buy/1, http://<public ip>/sell/1

@app.route('/api/<string:instrument>/<string:direction>/<int:units>', methods = ['GET'])
def place_trade(instrument, direction, units):
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + 'orders'

    params = {
        "order": {
            "side": direction,
            "units": str(units),
            # "instrument": "EUR_USD",
            "instrument": instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }

    response = requests.post(url, headers = header, json = params)
    broker_data = response.json()
    return broker_data
    


# get balance: http://<public ip>/api/balance/

@app.route('/api/balance/', methods = ['GET'])
def get_balance():
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + '/summary'
    response = requests.get(url, headers = header)
    broker_data = response.json()
    return broker_data['account']['balance']




if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = 80) # amazon ec2
    app.run() # local 

    
    




