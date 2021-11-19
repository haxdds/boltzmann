from src.exchange.data.trade import Trade
from typing import List

class Order:

    def __init__(self, id: float, pid: float, timestamp: float, symbol: str, side: str, type: str, qty: float, price: float=None):
        self.id = id
        self.pid = pid
        self.timestamp = timestamp
        self.symbol = symbol
        self.side = side
        self.type = type
        self.qty = qty
        self.price = price
        self.cost = qty * price if price != None else 0
        self.trades = []
        self._qty_filled = 0
        self._avg_fill_price = 0
        self._filled_cost = 0

    def cancel(self):
        # need to implement somehow
        pass

    def update(self):
        # need to implement 
        pass

    def filled(self) -> bool:
        return self.qty == self._qty_filled

    def qty_filled(self) -> float:
        return self._qty_filled

    def average_fill_price(self) -> float:
        return self._avg_fill_price

    def add_trades(self, trades: List[Trade]):
        self.trades.extend(trades)

        for trade in trades:
            self._filled_cost += trade.price * trade.qty
            self._qty_filled += trade.qty
        
        self._avg_fill_price = self._filled_cost / self._qty_filled

    def __str__(self):

        return f"t={self.timestamp}:{self.pid}:{self.type}:{self.id}:{self.side}:{self.symbol}:{self.qty}:{self.price if self.type == 'limit' else 0}"


        

    