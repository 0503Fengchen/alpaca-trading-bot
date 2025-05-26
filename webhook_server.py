from flask import Flask, request
from alpaca_trade_api.rest import REST
import os

app = Flask(__name__)

# 讀取環境變數
API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# 建立 Alpaca 交易物件
alpaca = REST(API_KEY, API_SECRET, BASE_URL)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("📩 收到資料：", data)

        # 檢查 secret token（如有啟用）
        if WEBHOOK_SECRET:
            if data.get("secret") != WEBHOOK_SECRET:
                print("🚫 驗證失敗！")
                return "Unauthorized", 403

        action = data.get("action")
        symbol = data.get("ticker")
        qty = int(data.get("qty", 1))

        print(f"📊 準備下單：{action} {qty} 股 {symbol}")

        if action == "buy":
            alpaca.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        elif action == "sell":
            alpaca.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        else:
            return "❗ 不支援的動作", 400

        return "✅ Order received", 200

    except Exception as e:
        print("❌ 錯誤發生：", e)
        return f"Server error: {e}", 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
