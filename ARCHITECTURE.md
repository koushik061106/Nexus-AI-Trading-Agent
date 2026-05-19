You are an expert quantitative developer, financial engineer and AI systems
architect. Build me a production-grade autonomous AI TRADING AGENT — not a
simple bot — with full agentic reasoning, self-learning, and capital protection.

Read every single requirement before writing one line of code.

═══════════════════════════════════════════════════════════════════════════
PROJECT: NEXUS AI TRADER v3.0 — Full Autonomous Trading Agent
═══════════════════════════════════════════════════════════════════════════

CORE PHILOSOPHY:
- Any profit is good profit — even 0.1% is a WIN
- Never lose more than 3% in one day — survival first
- Zero profit is acceptable — catastrophic loss is not
- The agent must THINK, PLAN, EXECUTE and LEARN autonomously
- Works with ANY capital — even Rs.500

═══════════════════════════════════════════════════════════════════════════
SECTION 1 — CRITICAL TECHNICAL REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════

LANGUAGE: Python 3.11.9 ONLY
WHY: Python 3.12+ breaks neo-api-client and many trading packages.
     Explicitly target Python 3.11.9. Add version check at startup:
     if sys.version_info < (3,11) or sys.version_info >= (3,12):
         raise SystemError("Requires Python 3.11.x exactly")

VIRTUAL ENVIRONMENT:
Create and use .venv inside project folder.
All packages installed in .venv — never global Python.

BROKER: Kotak Neo
Package: neo-api-client (install from GitHub NOT PyPI)
Install command: pip install git+https://github.com/Kotak-Neo/kotak-neo-api.git
WHY: neo-api-client is NOT on PyPI. Installing from PyPI always fails.
     Always use the GitHub URL above.

AI ENGINE: Groq API (primary) with OpenRouter fallback
WHY: Groq is free, fast, 6000 calls/day limit.
     Google Gemini free tier only allows ~50-100 calls/day — too low.
     OpenRouter free models give 404/429 errors frequently.

PRIMARY AI:
  API: https://api.groq.com/openai/v1/chat/completions
  Model: llama-3.3-70b-versatile
  Format: OpenAI-compatible (same as OpenRouter)
  Free limit: 6000 requests/day

FALLBACK AI CHAIN (try in order if Groq fails):
  1. groq: llama-3.3-70b-versatile
  2. groq: llama-3.1-8b-instant
  3. groq: gemma2-9b-it
  4. openrouter: (fetch live model list and try first free one)

JSON PARSING — CRITICAL FIX:
All AI models return JSON wrapped in ```json``` markdown blocks.
ALWAYS strip these before parsing:
  raw = raw.strip()
  for prefix in ["```json", "```"]:
      if raw.startswith(prefix): raw = raw[len(prefix):]
  if raw.endswith("```"): raw = raw[:-3]
  raw = raw.strip()

Always use max_tokens=1500 — responses get truncated at 500.
Always add "temperature": 0.1 for consistent JSON output.
Always tell AI in prompt: "Return RAW JSON only. No markdown.
No code blocks. No backticks. Just the JSON object itself."

FOLDER STRUCTURE — create ALL folders at startup:
  BASE_DIR / "data"
  BASE_DIR / "logs"
  BASE_DIR / "reviews"
  BASE_DIR / "data/charts"
Use: folder.mkdir(parents=True, exist_ok=True) for each.

═══════════════════════════════════════════════════════════════════════════
SECTION 2 — PROJECT FILE STRUCTURE
═══════════════════════════════════════════════════════════════════════════

nexus_v3/
├── config.py                   # All settings — user fills this
├── bot.py                      # Main entry point
├── backtest.py                 # Backtesting with yfinance
├── backtest_optimizer.py       # Parameter optimizer
├── setup.py                    # One-click setup script
├── START_BOT.bat               # Windows launcher
├── SETUP_GUIDE.txt             # Complete setup instructions
│
├── engine/
│   ├── __init__.py
│   ├── agent_loop.py           # CORE AGENT — goal-directed planning
│   ├── ai_engine.py            # Groq + fallback AI calls
│   ├── broker.py               # Kotak Neo API wrapper
│   ├── capital_allocator.py    # Smart capital splitting
│   ├── indicators.py           # RSI MACD BB EMA VWAP ATR
│   ├── risk_manager.py         # All 5 protection layers
│   ├── strategy.py             # 4-bucket strategy engine
│   ├── news_engine.py          # News + sentiment
│   ├── trade_memory.py         # Permanent trade memory
│   ├── learning_brain.py       # Daily/weekly AI reviews
│   ├── post_trade_analyser.py  # After-trade analysis
│   ├── mistake_detector.py     # Auto pattern detection
│   ├── strategy_scorer.py      # Performance scoring
│   ├── market_memory.py        # Market condition patterns
│   └── chart_analyser.py       # Visual chart analysis
│
├── utils/
│   ├── __init__.py
│   ├── logger.py               # File + terminal logging
│   ├── helpers.py              # Utility functions
│   └── telegram_notifier.py    # Phone alerts
│
├── data/
│   ├── trade_memory.json
│   ├── lifetime_stats.json
│   ├── learned_rules.json
│   ├── market_memory.json
│   ├── daily_allocation.json
│   └── optimal_params.json
│
├── logs/
│   └── nexus_YYYY-MM-DD.log    # Auto-deleted after 90 days
│
└── reviews/
    └── daily_review_YYYY-MM-DD.json

═══════════════════════════════════════════════════════════════════════════
SECTION 3 — CONFIG.PY COMPLETE STRUCTURE
═══════════════════════════════════════════════════════════════════════════

# ── KOTAK NEO ──────────────────────────────────────────────
CONSUMER_KEY  = ""        # App → More → Trade API → Create Application
MOBILE_NUMBER = ""        # +91XXXXXXXXXX with country code
UCC           = ""        # Client code from App → Profile
MPIN          = ""        # 6-digit MPIN set on Neo platform

# ── GROQ AI (Primary — Free 6000 calls/day) ────────────────
GROQ_API_KEY  = ""        # From console.groq.com → API Keys
GROQ_MODEL    = "llama-3.3-70b-versatile"

# ── OPENROUTER (Fallback only) ─────────────────────────────
OPENROUTER_API_KEY = ""   # From openrouter.ai → Keys
OPENROUTER_MODEL   = ""   # Auto-fetched from live free model list

# ── NEWS ────────────────────────────────────────────────────
NEWSAPI_KEY   = ""        # From newsapi.org — free tier

# ── TELEGRAM ALERTS (Optional) ─────────────────────────────
TELEGRAM_TOKEN   = ""     # From @BotFather on Telegram
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

═══════════════════════════════════════════════════════════════════════════
SECTION 4 — BROKER CONNECTIVITY
═══════════════════════════════════════════════════════════════════════════

Package: neo-api-client
Install: pip install git+https://github.com/Kotak-Neo/kotak-neo-api.git

Authentication flow:
  Step 1: NeoAPI(consumer_key=config.CONSUMER_KEY)
  Step 2: client.totp_login(mobilenumber, ucc, totp)
  Step 3: client.session_2fa(mpin)
  Step 4: Auto-renew session every 6 hours

Exchange segments:
  nse_cm  = NSE Cash equity (stocks)
  nse_fo  = NSE Futures and Options
  cde_fo  = Currency Derivatives
  mcx_fo  = MCX Commodities
  bse_cm  = BSE Cash equity

Product types:
  MIS   = Intraday (auto square-off by broker 3:20 PM)
  CNC   = Delivery (swing and position trades)
  NRML  = Normal (F&O overnight)

At startup:
  1. Download instrument master CSV from Kotak Neo
  2. Store all tokens in memory dict: {symbol: token}
  3. Fetch LIVE account balance — never assume capital
  4. Deployable = min(live_balance, MAX_CAPITAL_TO_USE)

Rate limiting:
  Max 10 API calls per second
  Implement token bucket rate limiter
  Retry any failed call 3 times with 2 second delay

Markets to trade:
  NSE Large Cap: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK,
                 SBIN, TATASTEEL, WIPRO, AXISBANK, BAJFINANCE
  NSE Low Price: TATASTEEL, IRFC, RECLTD, PNB, BANKBARODA,
                 NHPC, COALINDIA, SUZLON
  MCX Commodity: GOLD, GOLDPETAL, SILVER, CRUDEOIL, NATURALGAS
  Currency:      USDINR, EURINR, GBPINR
  F&O:           NIFTY current month, BANKNIFTY current month

═══════════════════════════════════════════════════════════════════════════
SECTION 5 — GROQ AI ENGINE
═══════════════════════════════════════════════════════════════════════════

Primary: Groq API
URL: https://api.groq.com/openai/v1/chat/completions
Auth: Bearer {GROQ_API_KEY}
Format: OpenAI-compatible JSON

def call_ai(prompt: str, max_tokens: int = 1500) -> str | None:
    """
    Call Groq with automatic fallback chain.
    Returns clean JSON string or None if all fail.
    """
    providers = [
        {
            "url": "https://api.groq.com/openai/v1/chat/completions",
            "key": config.GROQ_API_KEY,
            "models": ["llama-3.3-70b-versatile", "llama-3.1-8b-instant",
                       "gemma2-9b-it", "mixtral-8x7b-32768"]
        },
        {
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "key": config.OPENROUTER_API_KEY,
            "models": []  # Auto-fetch live free models
        }
    ]

    for provider in providers:
        for model in provider["models"]:
            try:
                headers = {
                    "Authorization": f"Bearer {provider['key']}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://nexus-trader.local",
                    "X-Title": "NEXUS AI Trader v3"
                }
                data = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.1
                }
                response = requests.post(
                    provider["url"], headers=headers,
                    json=data, timeout=30
                )
                result = response.json()

                if response.status_code == 429:
                    time.sleep(3)
                    continue
                if response.status_code == 404:
                    continue
                if "error" in result:
                    continue
                if "choices" not in result:
                    continue

                raw = result["choices"][0]["message"]["content"].strip()

                # Strip markdown code blocks
                for prefix in ["```json", "```"]:
                    if raw.startswith(prefix):
                        raw = raw[len(prefix):]
                if raw.endswith("```"):
                    raw = raw[:-3]
                raw = raw.strip()

                log.info(f"AI success: {provider['url']} / {model}")
                return raw

            except Exception as e:
                log.warning(f"{model}: {e}")
                continue

    log.error("All AI providers failed — defaulting to HOLD")
    return None

ALWAYS add to every prompt:
"Return RAW JSON only. No markdown. No code blocks.
 No backticks. No explanations. Just the JSON object."

THREE TYPES OF AI CALLS:

CALL TYPE 1 — MORNING ALLOCATION (9:10 AM):
Input: capital, market sentiment, VIX, SGX signal,
       top news, day of week, learned rules,
       market memory patterns
Output JSON:
{
  "date": "YYYY-MM-DD",
  "total_capital": float,
  "emergency_reserve": float,
  "deployable_capital": float,
  "allocation": {
    "SCALPING":  {"pct": 0-100, "amount": float, "reason": "string"},
    "INTRADAY":  {"pct": 0-100, "amount": float, "reason": "string"},
    "SWING":     {"pct": 0-100, "amount": float, "reason": "string"},
    "POSITION":  {"pct": 0-100, "amount": float, "reason": "string"}
  },
  "strategy_for_today": "SCALPING|INTRADAY|SWING|POSITION|MIXED",
  "overall_reasoning": "string under 200 chars",
  "risk_level_today": "VERY_LOW|LOW|MEDIUM|HIGH"
}

CALL TYPE 2 — AGENT TRADE DECISION (per cycle):
Input: goal, portfolio state, prices, indicators,
       news, positions, last 10 trades, learned rules,
       avoid_setups, favour_setups, market memory
Output JSON:
{
  "thinking": "step by step reasoning",
  "situation_assessment": "good|neutral|bad",
  "plan": ["action1", "action2", "action3"],
  "immediate_action": "BUY|SELL|HOLD|WAIT",
  "symbol": "SYMBOL or null",
  "quantity": integer or null,
  "wait_minutes": integer or null,
  "confidence": 1-10,
  "reasoning": "max 150 chars",
  "risk_notes": "any concerns"
}
Rule: confidence < 6 → override to HOLD
Rule: BUY + news BEARISH → downgrade to HOLD
Rule: 3 consecutive losses → force HOLD 30 min

CALL TYPE 3 — MIDDAY REBALANCE (12:00 PM):
Input: morning allocation, current bucket P&L
Output: should capital move between buckets?
{
  "rebalance_needed": true|false,
  "moves": [{"from": "SCALPING", "to": "INTRADAY",
             "amount": float, "reason": "string"}],
  "reasoning": "string"
}

═══════════════════════════════════════════════════════════════════════════
SECTION 6 — AGENT LOOP (Core Intelligence)
═══════════════════════════════════════════════════════════════════════════

This is what makes it an AGENT not just a bot.
Implement AgentLoop class in engine/agent_loop.py

The agent has a GOAL not just a question:
"Grow Rs.{capital} by market close today
 while protecting capital above all else."

Agent maintains state across entire trading day:
- Today's plan (3 steps ahead always)
- History of all actions taken today
- Results of each action
- Consecutive wins/losses counter
- Current confidence level

AGENT SELF-CORRECTION RULES:
- 2 consecutive losses on same symbol → avoid that symbol 2 hours
- 3 consecutive losses any symbol → pause all trading 30 minutes
- Plan step fails twice → abandon plan, call AI for new plan
- Win rate drops below 40% today → switch to SCALPING only
- Daily loss hits 50% of limit → reduce all position sizes by 50%

AGENT PLANNING CYCLE (every 30 seconds for scalping):

def agent_cycle(self):
    # 1. Update state with latest prices and results
    self.update_state()

    # 2. Check if current plan is still valid
    if self.plan_is_failing():
        self.plan = []  # Force replan

    # 3. Call AI with full context
    context = self.build_full_context()
    response = call_ai(context)

    # 4. Parse and validate decision
    decision = self.parse_decision(response)
    if decision["confidence"] < 6:
        decision["immediate_action"] = "HOLD"

    # 5. Execute immediate action
    result = self.execute(decision)

    # 6. Store result for next cycle
    self.action_history.append({
        "action": decision["immediate_action"],
        "result": result,
        "timestamp": datetime.now().isoformat()
    })

    # 7. Update plan — remove completed step
    if self.plan:
        self.plan.pop(0)

CONTEXT BUILT FOR EVERY AI CALL includes:
  - Today's goal and current P&L toward goal
  - All 3 strategy bucket states
  - Live prices for all watchlist
  - Technical indicators (RSI, MACD, BB, EMA, VWAP, ATR)
  - News sentiment per symbol (last 2 hours)
  - Current plan and progress
  - Last 10 actions and their results
  - ALL learned rules from learned_rules.json
  - Setups to avoid (from own loss history)
  - Setups to favour (from own win history)
  - Market memory patterns (top 5 relevant)
  - VIX level
  - Day of week and time of day
  - Strategy scores (which is performing best)

═══════════════════════════════════════════════════════════════════════════
SECTION 7 — SMART CAPITAL ALLOCATION
═══════════════════════════════════════════════════════════════════════════

CAPITAL TIERS:
  < Rs.1,000  → SCALPING only (1-2 cheap shares max)
  < Rs.5,000  → SCALPING + INTRADAY only
  < Rs.25,000 → All 4 strategies available
  Rs.25,000+  → Full deployment with F&O

find_tradeable_instruments(capital):
  Filter watchlist to stocks affordable with capital.
  Must be able to buy at least 1 share AND keep reserve.
  Sort by: liquidity first, then price fit.
  For Rs.500: return only stocks under Rs.400/share.
  Never suggest F&O/Currency if capital < Rs.5,000.

MORNING ALLOCATION EXAMPLES:

Rs.500 — bearish day:
  Reserve Rs.50 | SCALPING 100% = Rs.450
  INTRADAY 0% | SWING 0% | POSITION 0%

Rs.500 — bullish RBI rate cut day:
  Reserve Rs.50 | SCALPING 40% = Rs.180
  INTRADAY 60% = Rs.270 | SWING 0% | POSITION 0%

Rs.500 — Friday afternoon:
  Reserve Rs.50 | SCALPING 50% | INTRADAY 50%
  SWING 0% — NEVER carry overnight on micro account

Rs.10,000 — strong uptrend:
  Reserve Rs.1,000 | SCALPING 25% | INTRADAY 40%
  SWING 25% | POSITION 10%

REBALANCING after every closed trade:
  Scalping profit → 50% moves to INTRADAY bucket
  Intraday profit → 30% to SCALPING, 20% to SWING
  Bucket fully lost → CLOSE that bucket for today
  Up 1% for day → LOCK that gain, only risk excess

DAILY SCHEDULE:
  09:10 AM  Morning allocation AI call
  09:15 AM  Market opens — SCALPING deploys immediately
  09:15-11  Peak scalping window
  11-01:00  INTRADAY positions entered
  01-02:30  Review and take profits
  02:30 PM  Start closing INTRADAY
  03:00 PM  ALL INTRADAY CLOSED
  03:15 PM  Hard square-off — everything closed
  04:00 PM  Daily self-review
  Sunday PM Weekly deep review

═══════════════════════════════════════════════════════════════════════════
SECTION 8 — 4 STRATEGY BUCKETS
═══════════════════════════════════════════════════════════════════════════

Each bucket has its own capital, P&L, AI cycle, rules.
All 4 run simultaneously in separate threads.

⚡ SCALPING (Bucket A):
  Position size : max 40% of bucket per trade
  Target        : 0.1% to 0.5%
  Stop loss     : 0.3%
  Hold time     : 5 seconds to 30 minutes
  AI interval   : every 30 seconds
  Best stocks   : IRFC, TATASTEEL, RECLTD (low price, liquid)
  Special rules : 3 wins → next size +10%
                  1 loss → next size -20%

🌅 INTRADAY (Bucket B):
  Position size : max 60% of bucket per trade
  Target        : 0.5% to 2%
  Stop loss     : 0.3%
  Hold time     : 1-6 hours (MUST close by 3PM)
  AI interval   : every 2 minutes
  Order type    : MIS (auto square-off)
  Special rules : if profitable at 2:30 PM → close immediately

📈 SWING (Bucket C):
  Position size : max 50% of bucket
  Target        : 3-8% over days
  Stop loss     : 1%
  Hold time     : 1 day to 3 weeks
  AI interval   : every 30 minutes
  Order type    : CNC (delivery)
  Special rules : never enter on Friday afternoon
                  never enter on results day
                  minimum Rs.500 to use this bucket

🏦 POSITION (Bucket D):
  Position size : max 30% of bucket
  Target        : 10-25% over weeks
  Stop loss     : 5%
  Hold time     : weeks to months
  AI interval   : once per day
  Order type    : CNC (delivery)
  Minimum       : Rs.2,000 capital to use this bucket

═══════════════════════════════════════════════════════════════════════════
SECTION 9 — 5 PROTECTION LAYERS
═══════════════════════════════════════════════════════════════════════════

LAYER 1 — Per Trade (non-negotiable):
  Stop loss      : 0.3% below entry — ALWAYS
  Trailing stop  : 0.2% below highest price reached
  Min profit     : 0.1% — take profit at even Rs.0.50
  Max profit     : 2.0% — close, don't be greedy
  Time exit      : 90 minutes open with no profit → exit flat

LAYER 2 — Daily:
  Daily loss limit : 3% of capital (Rs.15 on Rs.500)
  When hit         : close ALL positions, STOP for day
  Profit lock      : once up 1% → lock that gain
                     only trade excess profits rest of day

LAYER 3 — Position Sizing:
  Micro (<Rs.1k)  : max 1-2 shares, no F&O, no currency
  Small (Rs.1k-5k): max 5 shares, no F&O
  Medium+         : ATR-based sizing
  Hard cap        : never more than 40% of bucket in one trade

LAYER 4 — Market Defense:
  VIX > 20             → scalping only, halve all sizes
  SGX Nifty down 1%+  → wait 30 min after open
  3 losses in a row   → pause all trading 30 minutes
  Very bearish news   → 100% cash, wait for reversal
  Results day for held stock → close before announcement

LAYER 5 — Auto Square-off:
  NSE positions  : ALL closed by 3:15 PM no exceptions
  MCX positions  : closed by 11:00 PM
  Internet drops : if disconnected > 2 min → emergency close all
  Manual override: Ctrl+C triggers graceful close + summary

═══════════════════════════════════════════════════════════════════════════
SECTION 10 — NEWS AND GLOBAL INTELLIGENCE
═══════════════════════════════════════════════════════════════════════════

NewsEngine class runs in background thread.
Fetch every 2 minutes from:
  RSS: Economic Times, Moneycontrol, LiveMint, NDTV Business
  NewsAPI.org: each watchlist stock + "India market"
  Google News RSS: NSE, BSE, RBI, Fed Reserve, crude oil

Score each headline:
  VERY_BULLISH / BULLISH / NEUTRAL / BEARISH / VERY_BEARISH

Maintain per-symbol sentiment (rolling 2-hour window).
Maintain market-wide sentiment score.

Monitor continuously:
  RBI policy announcements
  Fed Reserve decisions
  India CPI, GDP, IIP data
  US Non-Farm Payrolls
  Crude oil EIA inventory
  OPEC decisions
  Corporate results (check if watchlist stock has results today)
  FII/DII flow data
  SGX Nifty pre-market signal
  Dow Jones, S&P 500, NASDAQ previous close

News-driven actions:
  3+ BULLISH on one symbol in 30 min → strong buy signal
  RBI rate cut → increase INTRADAY% for banking stocks
  Crude drops 2% → watch aviation and paint stocks
  US futures deeply red → reduce all allocations 30%
  Results day for held stock → EXIT before announcement
  Global crisis → 100% cash immediately

═══════════════════════════════════════════════════════════════════════════
SECTION 11 — MEMORY AND SELF-LEARNING SYSTEM
═══════════════════════════════════════════════════════════════════════════

Every trade saved to data/trade_memory.json with:
{
  "trade_id": "uuid",
  "timestamp_entry": "ISO",
  "timestamp_exit": "ISO",
  "symbol": "TATASTEEL",
  "segment": "nse_cm",
  "strategy_bucket": "SCALPING",
  "action": "BUY",
  "quantity": 3,
  "entry_price": 141.20,
  "exit_price": 141.65,
  "exit_reason": "TRAILING_STOP_HIT",
  "pnl_rupees": 1.35,
  "pnl_percent": 0.32,
  "outcome": "WIN",
  "hold_minutes": 43,
  "market_context": {
    "vix": 13.4,
    "nifty_trend": "UP",
    "sentiment": "BULLISH",
    "time_of_day": "MORNING",
    "day_of_week": "TUESDAY",
    "consecutive_wins_before": 2,
    "consecutive_losses_before": 0
  },
  "technical": {
    "rsi_14": 58.3,
    "macd_signal": "BULLISH_CROSSOVER",
    "bb_position": "MIDDLE_TO_UPPER",
    "ema_9_vs_21": "ABOVE",
    "vwap_position": "ABOVE",
    "atr": 1.8,
    "volume_vs_avg": 1.4
  },
  "news_context": {
    "symbol_sentiment": "BULLISH",
    "market_sentiment": "BULLISH",
    "headlines": ["TATASTEEL export order"]
  },
  "ai_decision": {
    "confidence": 8,
    "reasoning": "Strong momentum with news catalyst",
    "plan_at_time": ["BUY TATASTEEL", "WAIT 10min", "SELL at target"]
  },
  "post_analysis": {
    "was_entry_good": null,
    "was_exit_good": null,
    "lesson_learned": null,
    "repeat_setup": null,
    "avoid_setup": null
  }
}

DAILY SELF-REVIEW at 4:00 PM:
Call AI with all today's trades + lifetime stats.
Ask: what worked, what failed, mistakes made,
     rules to add, tomorrow's adjustments.
Save to reviews/daily_review_YYYY-MM-DD.json

WEEKLY DEEP REVIEW every Sunday 8 PM:
Full week analysis, strategy scores,
watchlist changes, next week plan.
Generate weekly_improvement_report_YYYY-WW.txt

LEARNED RULES ENGINE:
data/learned_rules.json starts empty.
Grows as bot learns from own mistakes.
Example rules it might write itself:
  "Do not trade TATASTEEL after 2 PM — 20% win rate"
  "IRFC VWAP bounce in morning → 74% win rate"
  "Monday with bullish SGX → increase INTRADAY allocation"

Rules injected into EVERY AI call.
Rules validated weekly — if not helping → inactive.
Confidence < 4 → remove rule.
Confidence > 7 for 4 weeks → permanent rule.

MISTAKE PATTERNS auto-detected (no AI needed):
  Revenge trading: 3 BUYs within 10 min of stop loss
  Overtrading: >8 trades/hour with <40% win rate
  Holding losers: reached -0.2% before stop at -0.3%
  Exiting early: closed at 0.1% but moved 0.5% after
  Time-based losses: consistent losses in one time window
  Symbol addiction: >40% of trades in one symbol
  News blindness: losses within 30 min of opposite news

STRATEGY SCORER every 20 trades:
  Score = (Win Rate × 0.4) + (Profit Factor × 0.3)
        + (Sharpe × 0.2) + (Consistency × 0.1)
  8-10: EXCELLENT → increase allocation +10%
  6-7:  GOOD → maintain
  4-5:  AVERAGE → reduce -20%
  2-3:  POOR → reduce -50%
  0-1:  FAILING → suspend 7 days

═══════════════════════════════════════════════════════════════════════════
SECTION 12 — BACKTESTING SYSTEM
═══════════════════════════════════════════════════════════════════════════

File: backtest.py and backtest_optimizer.py
Data: yfinance (free, no API key)
NSE symbol format: "TATASTEEL.NS", "RELIANCE.NS"

Test these strategies on 1 year historical data:
  RSI Strategy: buy RSI < 35, sell RSI > 65
  MACD Strategy: buy bullish crossover, sell bearish
  VWAP Strategy: buy above VWAP, sell below
  Bollinger: buy lower band touch, sell upper band
  Combined: RSI + MACD confirmation required

For each show:
  Total return %, Win rate %, Max drawdown %,
  Sharpe ratio, Number of trades, Best/worst trade

Walk-forward validation (honest backtesting):
  Train Jan-Sep, Test Oct-Dec
  Prevents overfitting to historical data

Save best strategy to data/optimal_params.json
Bot uses these proven parameters for live trading.

CLI usage:
  python backtest.py TATASTEEL 2024-01-01 2024-12-31
  python backtest.py ALL 2024-01-01 2024-12-31
  python backtest_optimizer.py IRFC 2024-01-01 2024-12-31

═══════════════════════════════════════════════════════════════════════════
SECTION 13 — TELEGRAM ALERTS
═══════════════════════════════════════════════════════════════════════════

File: utils/telegram_notifier.py
Library: python-telegram-bot
Config: TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ENABLED

Send messages for:
  BUY trade: "⚡ BUY 3× IRFC @ Rs.141.20 | Cost: Rs.423 | SCALPING"
  SELL trade: "✅ SELL 3× IRFC @ Rs.141.65 | +Rs.1.35 (+0.32%)"
  Stop loss:  "🛑 STOP LOSS IRFC | -Rs.1.26 (-0.30%) | Capital safe"
  Daily sum:  "📊 Day end | +Rs.5.20 (+1.04%) | 8 trades | 75% wins"
  Emergency:  "🚨 Daily loss limit hit! All positions closed."
  Morning:    "🌅 NEXUS starting | Rs.450 deployed | Strategy: SCALPING"

Respond to commands:
  /status   → current positions and P&L
  /stop     → pause trading
  /resume   → resume trading
  /summary  → today's performance

Only send if TELEGRAM_ENABLED = True in config.

═══════════════════════════════════════════════════════════════════════════
SECTION 14 — LIVE TERMINAL DASHBOARD
═══════════════════════════════════════════════════════════════════════════

Use rich library. Refresh every 3 seconds.
Use rich.live — do NOT clear terminal each refresh.

┌─ NEXUS AI TRADER v3.0 ──────────────── 10:23:14 IST ───────────────┐
│  Capital: Rs.500 │ VIX: 13.4 │ Sentiment: 🟢 BULLISH │ Risk: LOW   │
├─ TODAY'S ALLOCATION ──────────────────────────────────────────────  ┤
│  🔒 Reserve  : Rs.50   (locked)                                      │
│  ⚡ SCALPING : Rs.450  (100%) │ P&L: +Rs.3.20  │ Wins:4  Loss:1    │
│  🌅 INTRADAY : Rs.0    ( 0%)  │ P&L: —          │ [SKIP today]      │
│  📈 SWING    : Rs.0    ( 0%)  │ P&L: —          │ [SKIP today]      │
├─ OPEN POSITIONS ──────────────────────────────────────────────────  ┤
│  ⚡ IRFC     3sh  Buy@Rs.141.20  Now:Rs.141.65  +Rs.1.35  +0.32% 🟢│
├─ AGENT PLAN ──────────────────────────────────────────────────────  ┤
│  Step 1: ✅ BUY IRFC (done)                                          │
│  Step 2: ⏳ WAIT 10 min for target                                   │
│  Step 3: 📋 SELL IRFC at 0.3%+ profit                               │
├─ DAILY TOTALS ────────────────────────────────────────────────────  ┤
│  Started: Rs.500 │ Now: Rs.505.20 │ +Rs.5.20 (+1.04%) 🟢            │
│  Locked: Rs.5.00 │ Trades: 6 │ Win Rate: 83%                        │
├─ SELF-LEARNING ───────────────────────────────────────────────────  ┤
│  Lifetime: 127 trades │ Win Rate: 68% │ Total P&L: +Rs.4,230        │
│  Active Rules: 12 │ Mistakes Avoided Today: 3                        │
│  Scores: ⚡8.2✅ 🌅6.5✅ 📈3.1⚠️ 🏦PAUSED❌                         │
├─ AI REASONING ────────────────────────────────────────────────────  ┤
│  [⚡ SCALPING] Holding IRFC — trailing stop protecting +0.32%       │
│  Next analysis: 28 seconds                                           │
├─ LATEST NEWS ─────────────────────────────────────────────────────  ┤
│  🟢 FII net buyers Rs.2,400Cr — market bullish                      │
│  🟡 Crude steady at $83 ahead of OPEC                               │
│  🟢 IRFC gets infrastructure order — positive catalyst              │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════
SECTION 15 — STARTUP SEQUENCE
═══════════════════════════════════════════════════════════════════════════

When bot.py is run:

1.  Check Python version == 3.11.x (error if not)
2.  Create all folders: data/ logs/ reviews/ data/charts/
3.  Validate config.py — no empty fields, no placeholders
4.  Print NEXUS v3.0 banner
5.  Test Groq API with simple call: "Reply OK"
6.  Test NewsAPI — fetch one headline
7.  Connect Kotak Neo → TOTP input → MPIN → verify
8.  Fetch LIVE account balance from Kotak
9.  Download instrument master CSV
10. Fetch initial prices for all watchlist
11. Calculate initial technical indicators
12. Load trade_memory.json, learned_rules.json
13. Load lifetime_stats.json
14. Print Systems Check table — all must be green
15. If PAPER_TRADING=True → show large warning banner
16. Run morning allocation AI call
17. Show today's allocation plan
18. Start all threads (price, news, strategies)
19. Start agent loop
20. Display live dashboard

═══════════════════════════════════════════════════════════════════════════
SECTION 16 — REQUIREMENTS.TXT
═══════════════════════════════════════════════════════════════════════════

# Core broker — MUST install from GitHub not PyPI
# pip install git+https://github.com/Kotak-Neo/kotak-neo-api.git

# AI and HTTP
requests>=2.25.1
groq

# Data and analysis
pandas>=2.0.0
numpy>=1.24.0
ta>=0.11.0
yfinance>=0.2.0
mplfinance>=0.12.0

# News
feedparser>=6.0.0
newsapi-python>=0.2.7

# Scheduling and utils
schedule>=1.2.0
pyotp>=2.9.0
python-dateutil>=2.8.0

# Display
rich>=14.0.0
colorlog>=6.0.0

# Alerts
python-telegram-bot>=20.0
pyttsx3>=2.90

# ML (for future upgrades)
scikit-learn>=1.0.0
xgboost>=1.7.0

═══════════════════════════════════════════════════════════════════════════
SECTION 17 — SETUP.PY (One-click installer)
═══════════════════════════════════════════════════════════════════════════

Create setup.py that does everything automatically:

1. Check Python 3.11 is installed
2. Create .venv virtual environment
3. Activate .venv
4. Install all packages from requirements.txt
5. Install neo-api-client from GitHub
6. Create all required folders
7. Create empty JSON files with correct structure
8. Print "Setup complete! Edit config.py then run START_BOT.bat"

═══════════════════════════════════════════════════════════════════════════
SECTION 18 — START_BOT.BAT (Windows launcher)
═══════════════════════════════════════════════════════════════════════════

@echo off
title NEXUS AI TRADER v3.0
color 0A
echo.
echo  ================================================
echo   NEXUS AI TRADER v3.0
echo   "Any profit is good — even 0.1 percent"
echo  ================================================
echo.
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python setup.py
)
echo Starting NEXUS Agent...
echo Press Ctrl+C to stop safely.
echo.
python bot.py
echo.
echo Bot stopped safely.
pause

═══════════════════════════════════════════════════════════════════════════
SECTION 19 — AUTO-CLEANUP
═══════════════════════════════════════════════════════════════════════════

Run at every startup:
  Delete log files older than 90 days
  Archive trade_memory.json to trade_memory_YYYY.json
    every January 1st (keep current year active)
  Never delete: learned_rules.json, market_memory.json,
    lifetime_stats.json, optimal_params.json

═══════════════════════════════════════════════════════════════════════════
DELIVERABLE REQUIREMENTS
═══════════════════════════════════════════════════════════════════════════

1. Create ALL files completely — zero placeholders
2. Zero "TODO" comments — every function fully implemented
3. Every file must be immediately runnable
4. Run python -m py_compile on every .py file to verify
5. Create requirements.txt with exact versions
6. Create START_BOT.bat for Windows double-click launch
7. Create setup.py for one-click installation
8. Create SETUP_GUIDE.txt with complete step-by-step
   including section: "Running with just Rs.500"
9. Print summary of all files with line counts when done

The final system must work by:
  1. User fills config.py with credentials
  2. Double-clicks START_BOT.bat
  3. Enters TOTP when asked
  4. Agent starts trading autonomously
  5. User receives Telegram alerts on phone
  6. User reads daily review at 4 PM

PAPER_TRADING = True by default always.
User must explicitly change to False for live trading.