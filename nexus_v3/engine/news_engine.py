class NewsEngine:
    def __init__(self):
        pass

    def get_sentiment_all(self):
        """Returns mock news sentiment for testing"""
        return {
            "RELIANCE": {"score": 0.8, "sentiment": "BULLISH"},
            "HDFCBANK": {"score": 0.2, "sentiment": "BEARISH"},
            "TCS": {"score": 0.6, "sentiment": "NEUTRAL"}
        }