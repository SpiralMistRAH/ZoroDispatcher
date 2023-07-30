import time
import requests
import hmac
import hashlib
import random
from values import api_key, api_secret
from wallets import addresses

from urllib.parse import urlencode, quote

api_url = "https://api.mexc.com"


def _get_server_time():
    return requests.request('get', f'{api_url}/api/v3/time').json()['serverTime']


def _sign_v3(api_secret, req_time, sign_params=None):
    if sign_params:
        sign_params = urlencode(sign_params, quote_via=quote)
        to_sign = f"{sign_params}&timestamp={req_time}"
    else:
        to_sign = f"timestamp={req_time}"
    sign = hmac.new(api_secret.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    return sign


def get_balance(api_key, api_secret, coin):
    req_time = _get_server_time()
    params = {
        "coin": coin,
        "timestamp": req_time
    }
    params["signature"] = _sign_v3(api_secret, req_time, params)

    headers = {
        "Content-Type": "application/json",
        "X-MEXC-APIKEY": api_key
    }
    response = requests.get(f"{api_url}/api/v3/capital/get/coins", headers=headers, params=params)

    if response.status_code == 200:
        coins = response.json()
        for coin in coins:
            if coin['coin'] == coin:
                return float(coin['total'])
    return None


def withdraw_funds(api_key, api_secret, coin, address, amount, network='Arbitrum One'):
    balance = get_balance(api_key, api_secret, coin)
    if balance is None or balance < amount:
        print(f"Insufficient balance to transfer {amount} {coin} to {address}")
        return None
        
    params = {
        "coin": coin,
        "network": network,
        "address": address,
        "amount": amount,
    }
    req_time = _get_server_time()
    params["signature"] = _sign_v3(api_secret, req_time, params)
    params["timestamp"] = req_time

    headers = {
        "Content-Type": "application/json",
        "X-MEXC-APIKEY": api_key
    }
    response = requests.post(f"{api_url}/api/v3/capital/withdraw/apply", headers=headers, params=params)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something Else:", err)

    return response.json()


def distribute_funds(api_key, api_secret, coin, addresses, min_amount, max_amount, network='Arbitrum One'):
    for address in addresses:
        amount = random.uniform(min_amount, max_amount)
        print(f"Distributing {amount} {coin} to {address}")
        print("api_key passed: " + api_key)
        response = withdraw_funds(api_key, api_secret, coin, address, amount, network)
        print(response)


if __name__ == "__main__":
    # Replace these with your own values
    api_key = api_key
    api_secret = api_secret
    coin = 'ETH'
    addresses = addresses  # Replace with the actual addresses
    min_amount = 0.129
    max_amount = 0.131

    distribute_funds(api_key, api_secret, coin, addresses, min_amount, max_amount, network="Arbitrum One")
# "testing"