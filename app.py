import time
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Cache duration: 600 seconds (10 minutes)
CACHE_TTL = 600

CURRENCY_CACHE = {"rates": None, "updated_at": 0}
CRYPTO_CACHE = {"rates": None, "updated_at": 0}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/rates", methods=["GET"])
def get_rates():
    """Fetch real-time fiat currency rates with 10-min caching."""
    now = time.time()
    if not CURRENCY_CACHE["rates"] or (now - CURRENCY_CACHE["updated_at"]) > CACHE_TTL:
        try:
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
            data = response.json()
            if data.get("result") == "success":
                CURRENCY_CACHE["rates"] = data["rates"]
                CURRENCY_CACHE["updated_at"] = now
        except Exception as e:
            if not CURRENCY_CACHE["rates"]:
                return jsonify({"error": "Failed to fetch live currency rates", "details": str(e)}), 500

    return jsonify(CURRENCY_CACHE["rates"])

@app.route("/api/crypto", methods=["GET"])
def get_crypto():
    """Fetch real-time crypto rates via Coinbase API with 10-min caching."""
    now = time.time()
    if not CRYPTO_CACHE["rates"] or (now - CRYPTO_CACHE["updated_at"]) > CACHE_TTL:
        try:
            response = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=USD", timeout=5)
            data = response.json()
            if "data" in data and "rates" in data["data"]:
                CRYPTO_CACHE["rates"] = data["data"]["rates"]
                CRYPTO_CACHE["updated_at"] = now
        except Exception as e:
            if not CRYPTO_CACHE["rates"]:
                return jsonify({"error": "Failed to fetch live crypto rates", "details": str(e)}), 500

    return jsonify(CRYPTO_CACHE["rates"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)