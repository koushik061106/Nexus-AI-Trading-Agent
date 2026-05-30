from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from datetime import datetime
import json
import asyncio
from graph import agent_graph, AgentState
import config

app = FastAPI(title="NEXUS AI Trading Agent", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://nexus-ai-trading-agent.vercel.app",
        "http://localhost:3000",
        "*"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {
        "status": "alive",
        "service": "NEXUS AI Trading Agent v3.0",
        "timestamp": datetime.now().isoformat(),
        "paper_trading": config.PAPER_TRADING
    }

def get_initial_state(capital: float = 500.0) -> dict:
    """Returns a dictionary matching the AgentState schema"""
    return {
        "capital": capital,
        "cash": capital * 0.9,
        "positions": {},
        "daily_pnl": 0.0,
        "live_prices": {},
        "indicators": {},
        "news_sentiment": {},
        "thinking": "",
        "plan": [],
        "current_step": 0,
        "situation": "neutral",
        "action": "HOLD",
        "symbol": None,
        "quantity": None,
        "confidence": 5,
        "reasoning": "",
        "action_history": [],
        "consecutive_losses": 0,
        "messages": []
    }

@app.get("/agent/stream")
async def stream_agent(capital: float = 500.0):
    async def generate():
        state = get_initial_state(capital)
        yield f"data: {json.dumps({'type': 'start', 'capital': capital})}\n\n"

        async for chunk in agent_graph.astream(state):
            node_name = list(chunk.keys())[0]
            node_state = chunk[node_name]

            payload = {
                "type": "update",
                "node": node_name,
                "action": node_state.get("action", "HOLD"),
                "symbol": node_state.get("symbol"),
                "quantity": node_state.get("quantity"),
                "thinking": node_state.get("thinking", ""),
                "reasoning": node_state.get("reasoning", ""),
                "plan": node_state.get("plan", []),
                "cash": node_state.get("cash", capital),
                "daily_pnl": node_state.get("daily_pnl", 0),
                "positions": node_state.get("positions", {}),
                "messages": node_state.get("messages", []),
                "confidence": node_state.get("confidence", 5),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(0.1)

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

@app.post("/agent/decide")
async def single_decision(capital: float = 500.0):
    state = get_initial_state(capital)
    result = await agent_graph.ainvoke(state)
    return {
        "action": result.get("action", "HOLD"),
        "symbol": result.get("symbol"),
        "quantity": result.get("quantity"),
        "reasoning": result.get("reasoning", ""),
        "confidence": result.get("confidence", 5),
        "daily_pnl": result.get("daily_pnl", 0.0),
        "cash": result.get("cash", capital),
        "positions": result.get("positions", {})
    }

@app.get("/portfolio")
async def portfolio():
    return {
        "timestamp": datetime.now().isoformat(),
        "paper_trading": config.PAPER_TRADING,
        "message": "Connect to live state for real data"
    }

@app.get("/agent/allocate")
async def morning_allocation(capital: float = 500.0):
    from engine.capital_allocator import CapitalAllocator
    allocator = CapitalAllocator()
    return allocator.allocate(capital)