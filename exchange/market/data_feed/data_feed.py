from pymitter import EventEmitter
from exchange.data.trade import Trade
from exchange.data.tick import Tick
from exchange.data.order import Order
from exchange.data.quote import Quote
from typing import List

class DataFeed:

    def __init__(self):
        self.feed = EventEmitter(wildcard=True)
        self.subscriptions = 0
    

    def subscribe(self):
        self.subscriptions += 1
        return self.feed

    def unsubscribe(self):
        self.subscriptions -= 1

    def publish_trades(self, trades: List[Trade]):

        for trade in trades:
            pid_one = trade.party_one_pid
            pid_two = trade.party_two_pid
            self.feed.emit(f"trade.{pid_one}", trade)
            self.feed.emit(f"trade.{pid_two}", trade)

    def publish_tick(self, tick: Tick):

        self.feed.emit("tick.*", tick)
    
    def publish_order(self, order: Order):
        
        self.feed.emit(f"order.{order.pid}", order)
    
    def publish_quote(self, quote: Quote):

        self.feed.emit("quote.*", quote)
