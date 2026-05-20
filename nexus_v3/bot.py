import os
import pyotp
from flask import Flask, jsonify
from flask_cors import CORS
from neo_api_client import NeoAPI
from groq import Groq

app = Flask(__name__)
CORS(app)

# ─── KOTAK NEO AUTHENTICATION ────────────────────────────────
def get_live_balance():
    try:
        consumer_key = os.getenv("KOTAK_CONSUMER_KEY")
        consumer_secret = os.getenv("KOTAK_CONSUMER_SECRET")
        mobile = os.getenv("KOTAK_MOBILE")
        password = os.getenv("KOTAK_PASSWORD")
        totp_secret = os.getenv("KOTAK_TOTP_SECRET")

        if not consumer_key:
            return 0.00 

        # Generate live Google Auth code
        current_otp = pyotp.TOTP(totp_secret).now()

        # Secure Handshake
        client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment='prod')
        client.login(mobilenum=mobile, password=password)
        client.session_2fa(OTP=current_otp)
        
        limits_data = client.margin()
        available_margin = limits_data.get('Net', {}).get('availableCash', 0.00)
        
        return float(available_margin)
    except Exception as e:
        print(f"Broker Auth Error: {e}")
        return 0.00 
# ─────────────────────────────────────────────────────────────

# ─── AI NEURAL ENGINE ────────────────────────────────────────
def get_ai_analysis():
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            return "AI Offline: Missing API Key"

        client = Groq(api_key=groq_key)
        
        # Ask Llama-3 to generate a live market thought
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Nexus, a quantitative trading AI. Give a 1-sentence mock analysis of the Indian stock market today."
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"
# ─────────────────────────────────────────────────────────────

@app.route('/')
def home():
    return "Nexus AI Engine is Live!"

@app.route('/api/data')
def get_data():
    # Fetch real bank balance and AI thought simultaneously
    real_balance = get_live_balance()
    ai_thought = get_ai_analysis()
    
    return jsonify({
        "status": "online",
        "net_pnl": real_balance,
        "latest_log": f"[AI_THOUGHT] {ai_thought}"
    })

# ─── START THE SERVER ────────────────────────────────────────
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
# ─────────────────────────────────────────────────────────────