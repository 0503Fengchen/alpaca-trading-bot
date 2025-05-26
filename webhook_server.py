from flask import Flask, request
from alpaca_trade_api.rest import REST
import os

app = Flask(__name__)

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

alpaca = REST(API_KEY, API_SECRET, BASE_URL)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("收到訊號：", data)

    action = data.get("action")
    symbol = data.get("ticker")
    qty = int(data.get("qty", 1))

    if action == "buy":
        alpaca.submit_order(symbol=symbol, qty=qty, side='buy', type='market', time_in_force='gtc')
    elif action == "sell":
        alpaca.submit_order(symbol=symbol, qty=qty, side='sell', type='market', time_in_force='gtc')

    return "✅ Order received", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
