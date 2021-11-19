class Quote:

    def __init__(self, symbol: str, timestamp: float, bid: float, bid_size: float, ask: float, ask_size: float):
        self.symbol = symbol
        self.timestamp = timestamp
        self.bid = bid
        self.bid_size = bid_size
        self.ask = ask
        self.ask_size = ask_size

