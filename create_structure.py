import os
import json
from pathlib import Path

base_dir = Path("c:/games/trading agent/nexus_v3")
base_dir.mkdir(parents=True, exist_ok=True)

folders = [
    "engine",
    "utils",
    "data",
    "logs",
    "reviews",
    "data/charts"
]

for folder in folders:
    (base_dir / folder).mkdir(parents=True, exist_ok=True)

files = [
    "config.py",
    "bot.py",
    "backtest.py",
    "backtest_optimizer.py",
    "START_BOT.bat",
    "SETUP_GUIDE.txt",
    "engine/__init__.py",
    "engine/agent_loop.py",
    "engine/ai_engine.py",
    "engine/broker.py",
    "engine/capital_allocator.py",
    "engine/indicators.py",
    "engine/risk_manager.py",
    "engine/strategy.py",
    "engine/news_engine.py",
    "engine/trade_memory.py",
    "engine/learning_brain.py",
    "engine/post_trade_analyser.py",
    "engine/mistake_detector.py",
    "engine/strategy_scorer.py",
    "engine/market_memory.py",
    "engine/chart_analyser.py",
    "utils/__init__.py",
    "utils/logger.py",
    "utils/helpers.py",
    "utils/telegram_notifier.py"
]

for file in files:
    (base_dir / file).touch(exist_ok=True)

json_files = {
    "data/trade_memory.json": [],
    "data/lifetime_stats.json": {},
    "data/learned_rules.json": [],
    "data/market_memory.json": {},
    "data/daily_allocation.json": {},
    "data/optimal_params.json": {}
}

for filepath, content in json_files.items():
    p = base_dir / filepath
    if not p.exists() or p.stat().st_size == 0:
        with open(p, 'w') as f:
            json.dump(content, f, indent=4)

print("Structure created successfully.")
