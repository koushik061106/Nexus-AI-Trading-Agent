import config
from typing import List, Dict

class CapitalAllocator:
    """
    Implements the SMART CAPITAL ALLOCATION (Section 7)
    """
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.live_capital = initial_capital
        
        # Always keep reserve locked
        self.reserve = initial_capital * config.EMERGENCY_RESERVE_PCT
        self.deployable = initial_capital - self.reserve
        
        self.buckets = {
            "SCALPING": 0.0,
            "INTRADAY": 0.0,
            "SWING": 0.0,
            "POSITION": 0.0
        }
        self.bucket_status = {
            "SCALPING": "ACTIVE",
            "INTRADAY": "ACTIVE",
            "SWING": "ACTIVE",
            "POSITION": "ACTIVE"
        }
        
    def get_allowed_strategies(self) -> List[str]:
        """
        CAPITAL TIERS:
        < Rs.1,000  → SCALPING only
        < Rs.5,000  → SCALPING + INTRADAY only
        < Rs.25,000 → All 4 strategies available
        Rs.25,000+  → Full deployment with F&O
        """
        if self.live_capital < 1000:
            return ["SCALPING"]
        elif self.live_capital < 5000:
            return ["SCALPING", "INTRADAY"]
        else:
            return ["SCALPING", "INTRADAY", "SWING", "POSITION"]

    def find_tradeable_instruments(self, watchlist: List[dict], capital_for_trade: float) -> List[dict]:
        """
        Filter watchlist to stocks affordable with capital.
        Must be able to buy at least 1 share AND keep reserve.
        Sort by: liquidity first, then price fit.
        For Rs.500: return only stocks under Rs.400/share.
        Never suggest F&O/Currency if capital < Rs.5,000.
        """
        tradeable = []
        max_price = capital_for_trade * config.MAX_POSITION_PCT
        
        # Specific rule for 500
        if self.live_capital <= 500:
            max_price = min(max_price, 400.0)
            
        for inst in watchlist:
            segment = inst.get('segment', 'nse_cm')
            
            # Never suggest F&O/Currency if capital < Rs.5,000
            if self.live_capital < 5000 and segment in ['nse_fo', 'cde_fo', 'mcx_fo']:
                continue
                
            price = inst.get('price', float('inf'))
            if price <= max_price:
                tradeable.append(inst)
                
        # Sort by liquidity first (mocked by volume), then price fit (lowest price first usually allows more shares)
        tradeable.sort(key=lambda x: (x.get('volume', 0), -x.get('price', 0)), reverse=True)
        return tradeable

    def rebalance_after_trade(self, bucket: str, pnl: float):
        """
        REBALANCING after every closed trade:
        Scalping profit → 50% moves to INTRADAY bucket
        Intraday profit → 30% to SCALPING, 20% to SWING
        Bucket fully lost → CLOSE that bucket for today
        Up 1% for day → LOCK that gain, only risk excess
        """
        self.live_capital += pnl
        
        # Lock 1% gain
        if (self.live_capital - self.initial_capital) / self.initial_capital >= config.DAILY_PROFIT_LOCK_PCT:
            self.reserve = self.initial_capital * (1 + config.DAILY_PROFIT_LOCK_PCT)
            
        if pnl > 0:
            if bucket == "SCALPING":
                to_intraday = pnl * 0.50
                self.buckets["SCALPING"] += (pnl - to_intraday)
                self.buckets["INTRADAY"] += to_intraday
            elif bucket == "INTRADAY":
                to_scalp = pnl * 0.30
                to_swing = pnl * 0.20
                self.buckets["INTRADAY"] += (pnl - to_scalp - to_swing)
                self.buckets["SCALPING"] += to_scalp
                self.buckets["SWING"] += to_swing
            else:
                self.buckets[bucket] += pnl
        else:
            self.buckets[bucket] += pnl
            if self.buckets[bucket] <= 0:
                self.bucket_status[bucket] = "CLOSED"
                self.buckets[bucket] = 0.0

    def apply_morning_allocation(self, allocation_dict: Dict):
        """
        Applies percentages from the morning AI call JSON.
        """
        allowed = self.get_allowed_strategies()
        self.deployable = self.live_capital - self.reserve
        
        for strategy, details in allocation_dict.items():
            if strategy in allowed and self.bucket_status[strategy] == "ACTIVE":
                pct = details.get("pct", 0) / 100.0
                self.buckets[strategy] = self.deployable * pct
            else:
                self.buckets[strategy] = 0.0
