import json
from datetime import datetime, timedelta
import logging
from engine.ai_engine import call_ai
import config

log = logging.getLogger(__name__)

class AgentLoop:
    """
    Core Intelligence (Section 6)
    The agent has a GOAL: Grow capital by market close while protecting capital above all else.
    """
    def __init__(self, capital: float):
        self.capital = capital
        self.goal = f"Grow Rs.{capital} by market close today while protecting capital above all else."
        self.plan = []
        self.action_history = []
        
        self.consecutive_losses_any = 0
        self.symbol_losses = {} # {symbol: count}
        self.avoid_symbols_until = {} # {symbol: datetime}
        self.pause_trading_until = None
        
        self.step_fails = 0
        self.win_rate = 1.0
        self.daily_loss_pct = 0.0
        
        self.force_scalping_only = False
        self.reduce_position_sizes = False

    def update_state(self):
        """1. Update state with latest prices and results"""
        now = datetime.now()
        
        # Cleanup expired avoids
        expired = [s for s, t in self.avoid_symbols_until.items() if now >= t]
        for s in expired:
            del self.avoid_symbols_until[s]
            
        if self.pause_trading_until and now >= self.pause_trading_until:
            self.pause_trading_until = None
            
        # Agent rule: Win rate drops below 40% today -> switch to SCALPING only
        wins = sum(1 for a in self.action_history if a.get('outcome') == 'WIN')
        total_closed = sum(1 for a in self.action_history if 'outcome' in a)
        if total_closed >= 5:
            self.win_rate = wins / total_closed
            if self.win_rate < 0.40:
                self.force_scalping_only = True
                
        # Agent rule: Daily loss hits 50% of limit -> reduce all position sizes by 50%
        if self.daily_loss_pct <= -(config.DAILY_LOSS_LIMIT_PCT / 2):
            self.reduce_position_sizes = True

    def plan_is_failing(self) -> bool:
        """2. Check if current plan is still valid. Plan step fails twice -> abandon plan"""
        if self.step_fails >= 2:
            self.step_fails = 0
            return True
        return False

    def build_full_context(self) -> str:
        """3. Call AI with full context"""
        context = {
            "goal": self.goal,
            "win_rate": self.win_rate,
            "plan": self.plan,
            "last_actions": self.action_history[-10:],
            "force_scalping": self.force_scalping_only,
            "reduce_size": self.reduce_position_sizes
            # In a real environment, prices, indicators, news, rules, market_memory are injected here
        }
        return json.dumps(context)

    def parse_decision(self, response: str) -> dict:
        """4. Parse and validate decision"""
        if not response:
            return {"immediate_action": "HOLD", "confidence": 0}
            
        try:
            decision = json.loads(response)
        except json.JSONDecodeError:
            return {"immediate_action": "HOLD", "confidence": 0}
            
        # Rule: confidence < 6 -> override to HOLD
        confidence = decision.get("confidence", 0)
        if confidence < 6:
            decision["immediate_action"] = "HOLD"
            
        # Optional: New plan provided by AI
        if decision.get("plan"):
            self.plan = decision.get("plan")
            
        return decision

    def execute(self, decision: dict) -> dict:
        """5. Execute immediate action"""
        action = decision.get("immediate_action", "WAIT")
        symbol = decision.get("symbol")
        
        if action in ["HOLD", "WAIT"]:
            return {"status": "SUCCESS", "details": "Held position"}
            
        if symbol in self.avoid_symbols_until:
            return {"status": "FAIL", "details": f"Symbol {symbol} is avoided"}
            
        if self.pause_trading_until:
            return {"status": "FAIL", "details": "Trading globally paused"}
            
        # Mock execution logic returning success
        return {"status": "SUCCESS", "details": f"Executed {action} on {symbol}"}

    def register_trade_outcome(self, symbol: str, outcome: str):
        """Called externally when a trade closes to track self-correction rules."""
        # Store outcome in the latest action history if possible
        if self.action_history:
            self.action_history[-1]["outcome"] = outcome

        if outcome == "LOSS":
            self.consecutive_losses_any += 1
            self.symbol_losses[symbol] = self.symbol_losses.get(symbol, 0) + 1
            
            # Rule: 2 consecutive losses on same symbol -> avoid that symbol 2 hours
            if self.symbol_losses[symbol] >= 2:
                self.avoid_symbols_until[symbol] = datetime.now() + timedelta(hours=2)
                self.symbol_losses[symbol] = 0
                
            # Rule: 3 consecutive losses any symbol -> pause all trading 30 minutes
            if self.consecutive_losses_any >= 3:
                self.pause_trading_until = datetime.now() + timedelta(minutes=30)
                self.consecutive_losses_any = 0
                
        elif outcome == "WIN":
            self.consecutive_losses_any = 0
            self.symbol_losses[symbol] = 0

    def agent_cycle(self):
        """The 7-step core agent planning cycle (every 30 seconds for scalping)"""
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
        if decision.get("confidence", 0) < 6:
            decision["immediate_action"] = "HOLD"

        # 5. Execute immediate action
        result = self.execute(decision)
        if result.get("status") == "FAIL":
            self.step_fails += 1
        else:
            self.step_fails = 0

        # 6. Store result for next cycle
        self.action_history.append({
            "action": decision.get("immediate_action"),
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

        # 7. Update plan — remove completed step
        if self.plan and result.get("status") == "SUCCESS":
            self.plan.pop(0)
