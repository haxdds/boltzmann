from src.exchange.data_feed.data_feed import DataFeed
from src.exchange.market.market import Market
from typing import Dict
class Exchange:

    def __init__(self, name: str):

        self.name = name 
        self.markets: Dict[str, Market] = {}
        self.market_data_feeds = {}
        self.pid=100

    def add_market(self, symbol:str):
        self.market_data_feeds[symbol] = DataFeed()
        self.markets[symbol] = Market(symbol, self.market_data_feeds[symbol])

    def get_data_feed(self, symbol):
        if symbol not in self.market_data_feeds:
            print(f"Invalid Market {symbol}")
            return
        
        self.pid += 1
        return self.market_data_feeds[symbol], self.pid

    def submit_order(self, pid: float, symbol: str, qty: float, side: str, type: str, price: float=None):
        if symbol not in self.markets:
            print(f"Invalid Market {symbol}")
            return

        return self.markets[symbol].submit_order(pid, type, side, qty, price)

    def get_latest_quote(self, symbol):
        if symbol not in self.markets:
            print(f"Invalid Market {symbol}")
            return

        return self.markets[symbol].get_latest_quote()

    def get_latest_tick(self, symbol):
        if symbol not in self.markets:
            print(f"Invalid Market {symbol}")
            return

        return self.markets[symbol].get_last_tick()

    

        


