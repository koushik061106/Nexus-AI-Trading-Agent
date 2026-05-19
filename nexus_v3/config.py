import os

# ── API KEYS (Do NOT hardcode anything here) ──────────────
CONSUMER_KEY  = os.getenv("CONSUMER_KEY")
MOBILE_NUMBER = os.getenv("MOBILE_NUMBER")
UCC           = os.getenv("UCC")
MPIN          = os.getenv("MPIN")

# ── AI MODELS ─────────────────────────────────────────────
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL   = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

# ── NEWS & ALERTS ────────────────────────────────────────
NEWSAPI_KEY      = os.getenv("NEWSAPI_KEY")
TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "true").lower() == "true"

# ── CAPITAL ─────────────────────────────────────────────────
TRADING_CAPITAL       = 500      # Bot reads LIVE balance from Kotak
MAX_CAPITAL_TO_USE    = 500      # Hard cap — never exceed this
EMERGENCY_RESERVE_PCT = 0.10     # Always keep 10% locked

# ── PROFIT PHILOSOPHY ───────────────────────────────────────
MIN_PROFIT_TARGET_PCT = 0.001    # 0.1% — take ANY profit this size
MAX_PROFIT_TARGET_PCT = 0.02     # 2.0% — don't be greedy
STOP_LOSS_PCT         = 0.003    # 0.3% — hard stop, non-negotiable
TRAILING_STOP_PCT     = 0.002    # 0.2% — locks profits automatically
DAILY_LOSS_LIMIT_PCT  = 0.03     # 3% — stop trading if hit
DAILY_PROFIT_LOCK_PCT = 0.01     # 1% — lock this gain once reached

# ── POSITIONS ───────────────────────────────────────────────
MAX_POSITION_PCT   = 0.40        # Max 40% of bucket per trade
MAX_OPEN_POSITIONS = 5           # Max simultaneous positions

# ── TIMING ──────────────────────────────────────────────────
PRICE_REFRESH_SEC    = 5         # Fetch prices every 5 seconds
NEWS_REFRESH_SEC     = 120       # Fetch news every 2 minutes
ALLOCATION_TIME      = "09:10"   # Morning allocation call
MIDDAY_CHECK_TIME    = "12:00"   # Midday rebalance check
INTRADAY_CLOSE_TIME  = "15:00"   # Start closing intraday
HARD_SQUAREOFF_TIME  = "15:15"   # Absolute deadline

# ── SAFETY ──────────────────────────────────────────────────
PAPER_TRADING        = True      # MUST be False to place real orders
                                 # Default True — user changes explicitly

# ── VOICE ALERTS ────────────────────────────────────────────
VOICE_ALERTS         = False     # Set True to enable spoken alerts
