from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional
import config
from engine.ai_engine import call_ai
from engine.broker import BrokerClient
from engine.news_engine import NewsEngine
from engine.indicators import calculate_indicators

# ── AGENT STATE DEFINITION ───────────────────────────
class AgentState(TypedDict):
    capital: float
    cash: float
    positions: dict
    daily_pnl: float
    live_prices: dict
    indicators: dict
    news_sentiment: dict
    thinking: str
    plan: List[str]
    current_step: int
    situation: str
    action: str
    symbol: Optional[str]
    quantity: Optional[int]
    confidence: int
    reasoning: str
    action_history: List[dict]
    consecutive_losses: int
    messages: List[str]

# ── GRAPH NODES ──────────────────────────────────────

def fetch_market_data(state: AgentState) -> AgentState:
    """Node 1: Fetch live prices and indicators"""
    try:
        broker = BrokerClient()
        prices = broker.get_all_prices()
        indicators = calculate_indicators(prices)
        state["live_prices"] = prices or {}
        state["indicators"] = indicators or {}
    except Exception as e:
        state["messages"].append(f"Market fetch error: {str(e)}")
    return state

def fetch_news(state: AgentState) -> AgentState:
    """Node 2: Get latest news and sentiment"""
    try:
        news = NewsEngine()
        state["news_sentiment"] = news.get_sentiment_all() or {}
    except Exception as e:
        state["messages"].append(f"News fetch error: {str(e)}")
    return state

def agent_think(state: AgentState) -> AgentState:
    """Node 3: Core AI reasoning via Gemini"""
    prompt = f"""You are NEXUS AI Trading Agent.
GOAL: Grow Rs.{state['capital']} today.
PORTFOLIO: Cash: Rs.{state['cash']}, Daily P&L: Rs.{state['daily_pnl']}
LIVE PRICES: {state['live_prices']}

Return RAW JSON only. No markdown formatting or backticks:
{{
  "thinking": "step by step reasoning",
  "action": "BUY|SELL|HOLD",
  "symbol": "SYMBOL or null",
  "quantity": 1,
  "confidence": 1-10,
  "reasoning": "max 150 chars"
}}"""

    response = call_ai(prompt)
    if response:
        import json
        try:
            decision = json.loads(response)
            state["thinking"] = decision.get("thinking", "")
            state["action"] = decision.get("action", "HOLD")
            state["symbol"] = decision.get("symbol")
            state["quantity"] = decision.get("quantity")
            state["confidence"] = decision.get("confidence", 5)
            state["reasoning"] = decision.get("reasoning", "")
        except Exception:
            state["action"] = "HOLD"
            state["reasoning"] = "JSON parse error fallback"

    return state

def execute_trade(state: AgentState) -> AgentState:
    """Node 4: Execute the trade decision"""
    action = state["action"]
    symbol = state["symbol"]
    quantity = state["quantity"]

    if action == "BUY" and symbol and quantity:
        if config.PAPER_TRADING:
            price = state["live_prices"].get(symbol, 0)
            cost = price * quantity
            if state["cash"] - cost >= 50:
                state["cash"] -= cost
                state["positions"][symbol] = {"qty": quantity, "avg": price}
                state["messages"].append(f"[PAPER] BOUGHT {quantity}x {symbol}")

    elif action == "SELL" and symbol:
        if symbol in state["positions"]:
            price = state["live_prices"].get(symbol, 0)
            pos = state["positions"][symbol]
            pnl = (price - pos["avg"]) * pos["qty"]
            state["cash"] += price * pos["qty"]
            state["daily_pnl"] += pnl
            del state["positions"][symbol]
            state["messages"].append(f"[PAPER] SOLD {symbol} P&L: Rs.{pnl:.2f}")

    return state

def should_continue(state: AgentState) -> str:
    """Routing: keep trading or end session?"""
    from datetime import datetime
    now = datetime.now()
    if now.hour >= 15 and now.minute >= 15:
        return "end"
    if state["daily_pnl"] < -(state["capital"] * 0.03):
        return "end"
    return "continue"

# ── BUILD THE COMPILED GRAPH ────────────────────────
def build_agent_graph():
    graph = StateGraph(AgentState)
    graph.add_node("fetch_market", fetch_market_data)
    graph.add_node("fetch_news", fetch_news)
    graph.add_node("think", agent_think)
    graph.add_node("execute", execute_trade)

    graph.set_entry_point("fetch_market")
    graph.add_edge("fetch_market", "fetch_news")
    graph.add_edge("fetch_news", "think")
    graph.add_edge("think", "execute")

    graph.add_conditional_edges(
        "execute",
        should_continue,
        {"continue": "fetch_market", "end": END}
    )
    return graph.compile()

agent_graph = build_agent_graph()