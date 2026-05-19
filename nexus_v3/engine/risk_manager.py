import config
from datetime import datetime, time, timedelta

class RiskManager:
    """
    Implements the 5 Protection Layers detailed in Section 9 of the architecture.
    """
    
    def __init__(self):
        self.daily_starting_capital = 0.0
        self.current_capital = 0.0
        self.daily_peak_capital = 0.0
        self.profit_locked_for_day = False
        self.trading_paused_until = None
        self.consecutive_losses = 0
        
    def set_daily_capital(self, capital: float):
        """Initialize the daily tracking parameters."""
        self.daily_starting_capital = capital
        self.current_capital = capital
        self.daily_peak_capital = capital
        self.profit_locked_for_day = False
        self.consecutive_losses = 0
        self.trading_paused_until = None

    # ── LAYER 1: Per Trade (non-negotiable) ─────────────────────────
    def check_trade_exit(self, position: dict) -> str | None:
        """
        Check if an open position needs to be closed based on per-trade rules.
        position dict should contain:
        'entry_price', 'current_price', 'highest_price', 'lowest_price', 'open_time', 'direction' ('BUY'/'SELL')
        Returns reason for exit or None if hold.
        """
        entry = position.get('entry_price', 0.0)
        current = position.get('current_price', 0.0)
        highest = position.get('highest_price', current)
        open_time = position.get('open_time', datetime.now())
        direction = position.get('direction', 'BUY')
        
        if entry <= 0:
            return None
            
        # Calculate P&L %
        if direction == 'BUY':
            pnl_pct = (current - entry) / entry
            high_pct = (highest - entry) / entry
            drawdown_from_high = (highest - current) / highest if highest > 0 else 0
        else: # SHORT
            lowest = position.get('lowest_price', current)
            pnl_pct = (entry - current) / entry
            high_pct = (entry - lowest) / entry
            drawdown_from_high = (current - lowest) / lowest if lowest > 0 else 0
            
        # 1. Stop loss: 0.3% below entry — ALWAYS
        if pnl_pct <= -config.STOP_LOSS_PCT:
            return "STOP_LOSS_HIT"
            
        # 2. Trailing stop: 0.2% below highest price reached
        if high_pct > 0 and drawdown_from_high >= config.TRAILING_STOP_PCT:
            return "TRAILING_STOP_HIT"
            
        # 3. Max profit: 2.0% — close, don't be greedy
        if pnl_pct >= config.MAX_PROFIT_TARGET_PCT:
            return "MAX_PROFIT_HIT"
            
        # 4. Time exit: 90 minutes open with no profit → exit flat
        if pnl_pct <= 0:
            minutes_open = (datetime.now() - open_time).total_seconds() / 60.0
            if minutes_open >= 90:
                return "TIME_EXIT_NO_PROFIT"
                
        # 5. Min profit: 0.1% — take profit at even Rs.0.50 
        # (This rule tells the agent it *can* take profit, but we don't automatically trigger it here unless explicitly needed)
        
        return None

    # ── LAYER 2: Daily ──────────────────────────────────────────────
    def check_daily_limits(self, current_capital: float) -> str | None:
        """
        Updates daily peak and checks limits.
        Returns 'STOP_TRADING' or 'PROFIT_LOCK_HIT' if limits are hit.
        """
        self.current_capital = current_capital
        if self.current_capital > self.daily_peak_capital:
            self.daily_peak_capital = self.current_capital
            
        if self.daily_starting_capital <= 0:
            return None
            
        daily_pnl_pct = (self.current_capital - self.daily_starting_capital) / self.daily_starting_capital
        
        # Daily loss limit : 3% of capital
        if daily_pnl_pct <= -config.DAILY_LOSS_LIMIT_PCT:
            return "DAILY_LOSS_LIMIT_HIT"
            
        # Profit lock: once up 1% → lock that gain
        if daily_pnl_pct >= config.DAILY_PROFIT_LOCK_PCT:
            self.profit_locked_for_day = True
            
        # Only trade excess profits if locked
        if self.profit_locked_for_day:
            profit_locked_capital = self.daily_starting_capital * (1 + config.DAILY_PROFIT_LOCK_PCT)
            if self.current_capital < profit_locked_capital:
                return "PROFIT_LOCK_HIT"
                
        return None

    # ── LAYER 3: Position Sizing ────────────────────────────────────
    def get_max_position_size(self, capital_bucket: float, price: float) -> int:
        """
        Returns max number of shares to buy.
        Micro (<Rs.1k)  : max 1-2 shares
        Small (Rs.1k-5k): max 5 shares
        Medium+         : ATR-based sizing (placeholder, currently assumes max by capital bucket)
        Hard cap        : never more than 40% of bucket
        """
        if price <= 0:
            return 0
            
        if config.TRADING_CAPITAL < 1000:
            max_shares = 2
        elif config.TRADING_CAPITAL < 5000:
            max_shares = 5
        else:
            # Placeholder for ATR sizing, defaulting to max possible
            max_shares = int(capital_bucket / price)
            
        # Hard cap: never more than 40% of bucket in one trade
        max_investment = capital_bucket * config.MAX_POSITION_PCT
        shares_by_cap = int(max_investment / price)
        
        return min(max_shares, shares_by_cap)
        
    def can_trade_fno_or_currency(self) -> bool:
        """Micro/Small accounts (<5k) cannot trade F&O or currency."""
        return config.TRADING_CAPITAL >= 5000

    # ── LAYER 4: Market Defense ─────────────────────────────────────
    def check_market_defense(self, vix: float, sgx_nifty_pct: float, news_sentiment: str, result_day: bool) -> dict:
        """
        Returns defense actions dict based on market conditions.
        """
        defense = {
            "scalping_only": False,
            "halve_sizes": False,
            "pause_trading": False,
            "cash_100_pct": False,
            "close_position": False
        }
        
        # Check if trading is currently paused due to consecutive losses
        if self.trading_paused_until and datetime.now() < self.trading_paused_until:
            defense["pause_trading"] = True
            
        # VIX > 20 → scalping only, halve all sizes
        if vix > 20:
            defense["scalping_only"] = True
            defense["halve_sizes"] = True
            
        # SGX Nifty down 1%+ → wait 30 min after open
        if sgx_nifty_pct <= -1.0:
            now = datetime.now().time()
            market_open = time(9, 15)
            thirty_min_after = time(9, 45)
            if market_open <= now < thirty_min_after:
                defense["pause_trading"] = True
                
        # Very bearish news → 100% cash, wait for reversal
        if news_sentiment == "VERY_BEARISH":
            defense["cash_100_pct"] = True
            
        # Results day for held stock → close before announcement
        if result_day:
            defense["close_position"] = True
            
        return defense
        
    def register_trade_result(self, outcome: str):
        """
        Track wins and losses to pause trading on 3 consecutive losses.
        """
        if outcome == "LOSS":
            self.consecutive_losses += 1
            if self.consecutive_losses >= 3:
                self.trading_paused_until = datetime.now() + timedelta(minutes=30)
                self.consecutive_losses = 0 # reset after pause
        elif outcome == "WIN":
            self.consecutive_losses = 0

    # ── LAYER 5: Auto Square-off ────────────────────────────────────
    def check_auto_squareoff(self, is_mcx: bool = False) -> bool:
        """
        NSE positions : ALL closed by 3:15 PM (from config)
        MCX positions : closed by 11:00 PM
        Returns True if it's time to square off.
        """
        now = datetime.now().time()
        
        if is_mcx:
            hard_sq_time = time(23, 0)
        else:
            h, m = map(int, config.HARD_SQUAREOFF_TIME.split(':'))
            hard_sq_time = time(h, m)
            
        if now >= hard_sq_time:
            return True
            
        return False
        
    def is_internet_dropped(self, last_ping_time: datetime) -> bool:
        """
        If disconnected > 2 min → emergency close all
        """
        if (datetime.now() - last_ping_time).total_seconds() > 120:
            return True
        return False
