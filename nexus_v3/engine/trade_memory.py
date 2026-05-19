import json
import uuid
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)

class TradeMemory:
    """
    Handles read/writes of trade history (Section 11)
    """
    def __init__(self, data_dir: str = "data"):
        self.file_path = Path(data_dir) / "trade_memory.json"
        self.trades = []
        self.load()

    def load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r") as f:
                    content = f.read().strip()
                    if content:
                        self.trades = json.loads(content)
            except Exception as e:
                log.error(f"Failed to load trade memory: {e}")
                self.trades = []
        else:
            self.trades = []
            self.save()

    def save(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.trades, f, indent=2)
        except Exception as e:
            log.error(f"Failed to save trade memory: {e}")

    def add_trade(self, trade_data: dict) -> str:
        """Adds a trade to memory and persists to disk"""
        if "trade_id" not in trade_data:
            trade_data["trade_id"] = str(uuid.uuid4())
            
        if "timestamp_exit" not in trade_data:
            trade_data["timestamp_exit"] = datetime.now().isoformat()
            
        self.trades.append(trade_data)
        self.save()
        return trade_data["trade_id"]

    def get_trades_today(self) -> list:
        today = datetime.now().date().isoformat()
        return [t for t in self.trades if t.get("timestamp_entry", "").startswith(today)]
