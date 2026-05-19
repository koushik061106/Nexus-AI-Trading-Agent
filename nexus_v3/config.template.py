CONSUMER_KEY  = ""        # App → More → Trade API → Create Application
MOBILE_NUMBER = ""        # +91XXXXXXXXXX with country code
UCC           = ""        # Client code from App → Profile
MPIN          = ""        # 6-digit MPIN set on Neo platform

# ── GROQ AI (Primary — Free 6000 calls/day) ────────────────
GROQ_API_KEY  = ""        # From console.groq.com → API Keys
GROQ_MODEL    = ""

# ── OPENROUTER (Fallback only) ─────────────────────────────
OPENROUTER_API_KEY = ""   # From openrouter.ai → Keys
OPENROUTER_MODEL   = ""   # Auto-fetched from live free model list

# ── NEWS ────────────────────────────────────────────────────
NEWSAPI_KEY   = ""        # From newsapi.org — free tier

# ── TELEGRAM ALERTS (Optional) ─────────────────────────────
TELEGRAM_TOKEN   =""     # From @BotFather on Telegram
TELEGRAM_CHAT_ID = ""     # From @userinfobot on Telegram
TELEGRAM_ENABLED = False  # Set True when configured

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