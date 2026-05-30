from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
# Initialize the API
app = FastAPI()

# Security Handshake: Allow React to request data from this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def health():
    return {
        "status": "alive", 
        "timestamp": datetime.now().isoformat()
    }
# This is the "Endpoint". React will visit localhost:8000/api/data to get this!
@app.get("/api/data")
def get_dashboard_data():
    return {
        "botStatus": "Online",
        "stats": [
            { "title": "Total Trades", "value": "142", "color": "#7ee787" },
            { "title": "Win Rate", "value": "68.5%", "color": "#7ee787" },
            { "title": "Active Pairs", "value": "BTC/USD", "color": "#58a6ff" },
            { "title": "24h Profit", "value": "+$412.50", "color": "#7ee787" }
        ],
        "recentTrades": [
            { "time": "10:14:02 AM", "pair": "BTC/USD", "type": "BUY", "price": "$64,230.00", "status": "Executed" },
            { "time": "09:45:11 AM", "pair": "ETH/USD", "type": "SELL", "price": "$3,450.25", "status": "Executed" },
            { "time": "08:12:05 AM", "pair": "SOL/USD", "type": "BUY", "price": "$142.10", "status": "Executed" },
            { "time": "07:30:00 AM", "pair": "ADA/USD", "type": "BUY", "price": "$0.45", "status": "Pending" }
        ]
    }