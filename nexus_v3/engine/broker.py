import config

class BrokerClient:
    def __init__(self):
        self.is_paper = getattr(config, 'PAPER_TRADING', True)

    def get_all_prices(self):
        """Returns mock live prices for testing"""
        return {
            "RELIANCE": 2950.50,
            "HDFCBANK": 1440.00,
            "TCS": 3980.25
        }

    def place_order(self, symbol, action, quantity):
        """Mocks placing a real order"""
        print(f"BROKER: {action} {quantity} of {symbol}")
        return True