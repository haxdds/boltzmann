from src.exchange.data.quote import Quote
from lob.order_book import OrderBook
from src.exchange.data.tick import Tick
from src.exchange.data.trade import Trade
from src.exchange.data.order import Order
from src.exchange.data_feed.data_feed import DataFeed

class Market:

    def __init__(self, symbol:str, data_feed: DataFeed, min_tick_size=0.01):
        self._symbol = symbol
        self.__min_tick_size = min_tick_size
        self.book: OrderBook = OrderBook(min_tick_size)
        self.timestamp = 0
        self.__tick_number = 0
        self.market_data_feed = data_feed
    
    def submit_order(self, pid: float, type: str, side: str, qty: float, price: float=None, time_in_force: str='gtc'):
        
        if side != 'sell' and side != 'buy':
            print("Invalid Order: side: {side} --> Order Rejected")
            return    

        if qty <= 0:
            print("Invalid Order: qty <= 0 --> Order Rejected") 
            return

        if type != 'limit' and type != 'market':
            print("Invalid Order: type:{type} --> Order Rejected")
            return 

        side = 'ask' if side == 'sell' else 'bid'

        order_data = {
            'tid': pid, 
            'type': type,
            'side': side,
            'qty': qty}

        
        if type == 'limit':
            if price <= 0:
                print("Invalid Order: price <= 0 --> Order Rejected")
                return
            order_data['price'] = price

        trades, order_in_book = self.book.processOrder(order_data)

        order_id = order_in_book['idNum'] if order_in_book else None

        order = Order(order_id, pid, self.timestamp, self.symbol, side, type, qty, price)

        parsed_trades = Trade.parse_trades(trades)
        
        self.market_data_feed.publish_order(order)
        self.market_data_feed.publish_trades(parsed_trades)

    
    def increment_market_time(self):
        self.timestamp += 1
        self.book.updateTime()

        quote = self.get_latest_quote()
        tick = self.get_last_tick()

        self.market_data_feed.publish_quote(quote)
        self.market_data_feed.publish_tick(tick)
            
            
    @property
    def lob_time(self):
        return self.book.time


    @property
    def symbol(self):
        return self._symbol

    @property
    def tick_size(self):
        return self.__min_tick_size


    def get_latest_quote(self):
        # BBO
        bid = self.book.getBestBid()
        ask = self.book.getBestAsk()
        bid_size = self.book.getVolumeAtPrice(bid)
        ask_size = self.book.getVolumeAtPrice(ask)
        time = self.timestamp
        return Quote(self.symbol, time, bid, bid_size, ask, ask_size)

    def get_last_tick(self):
        
        time = self.timestamp
        last_tick = self.book.lastTick
        self.__tick_number += 1

        return Tick(self.__tick_number, self.symbol, time, last_tick)
