import os
from pathlib import Path
import pyotp
from flask import Flask, jsonify
from flask_cors import CORS
from neo_api_client import NeoAPI
app = Flask(__name__)
CORS(app)

# ─── KOTAK NEO AUTHENTICATION ────────────────────────────────
def get_live_balance():
    try:
        # Pull secure credentials from Render
        consumer_key = os.getenv("KOTAK_CONSUMER_KEY")
        consumer_secret = os.getenv("KOTAK_CONSUMER_SECRET")
        mobile = os.getenv("KOTAK_MOBILE")
        password = os.getenv("KOTAK_PASSWORD")
        totp_secret = os.getenv("KOTAK_TOTP_SECRET") # <--- Your Google Auth setup key

        if not consumer_key:
            return 777.77 

        # 1. Generate the live 6-digit code right now!
        current_otp = pyotp.TOTP(totp_secret).now()

        # 2. Initialize and Login
        client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod')
        client.login(mobilenum=mobile, password=password)
        client.session_2fa(OTP=current_otp) # <--- Pass the live code to Kotak
        
        # 3. Fetch Balance
        limits_data = client.margin()
        available_margin = limits_data.get('Net', {}).get('availableCash', 999.99)
        
        return float(available_margin)

    except Exception as e:
        print(f"Broker Auth Error: {e}")
        return 0.00 
# ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return "Nexus AI Bot is Live and Running!"

@app.route('/api/data')
def get_data():
    real_balance = get_live_balance()
    
    return jsonify({
        "status": "online",
        "net_pnl": real_balance,
        "latest_log": "Establishing secure handshake with Kotak Neo..."
    })
    # ─── START THE SERVER ────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# ─────────────────────────────────────────────────────────────