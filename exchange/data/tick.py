class Tick:

    def __init__(self, id: float, symbol: str, timestamp: float, price: float, size: float=0):
        self.id = id
        self.symbol = symbol
        self.timestamp = timestamp
        self.price = price
        self.size = size

    