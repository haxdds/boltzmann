class PortfolioHolding:

    def __init__(self, symbol: str, price: float, quantity: float, side: str):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side # 'long', 'short'
        self.price = price
        self.position_value = self.quantity * self.price

    def update_position_value(self, price):
        self.price = price
        self.position_value = self.price * self.quantity
        return self.position_value

class Portfolio:

    def __init__(self, pid: float, funding: float):
        self.pid = pid
        self.account_value = funding
        self.account_cash = funding
        self.holdings_value = 0

        self.holdings = {}