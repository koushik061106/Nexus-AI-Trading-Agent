# ── KOTAK NEO ──────────────────────────────────────────────
CONSUMER_KEY  = "c050533b-4204-4cfa-b0e0-71b4675a646c"        # App → More → Trade API → Create Application
MOBILE_NUMBER = "6301593052"        # +91XXXXXXXXXX with country code
UCC           = "W63SG"        # Client code from App → Profile
MPIN          = "000000"        # 6-digit MPIN set on Neo platform

# ── GROQ AI (Primary — Free 6000 calls/day) ────────────────
GROQ_API_KEY  = "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"        # From console.groq.com → API Keys
GROQ_MODEL    = "llama-3.3-70b-versatile"

# ── OPENROUTER (Fallback only) ─────────────────────────────
OPENROUTER_API_KEY = "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"   # From openrouter.ai → Keys
OPENROUTER_MODEL   = ""   # Auto-fetched from live free model list

# ── NEWS ────────────────────────────────────────────────────
NEWSAPI_KEY   = "pub_ba0ad0d3671e48059a4df2c0e981f3a2"        # From newsapi.org — free tier

# ── TELEGRAM ALERTS (Optional) ─────────────────────────────
TELEGRAM_TOKEN   ="8512845944:AAGy5ihE107pPnx_bqAKBgpZFRIZHScB2IE"     # From @BotFather on Telegram
TELEGRAM_CHAT_ID = "7940314762"     # From @userinfobot on Telegram
TELEGRAM_ENABLED = True  # Set True when configured

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
