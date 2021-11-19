from src.exchange.exchange import Exchange

# Create a LOB object
exchange = Exchange("NYSE")
exchange.add_market("ABC")

feed, pid = exchange.get_data_feed("ABC")
feed2, pid2 = exchange.get_data_feed("ABC")

@feed.feed.on(f"trade.{pid}")
def OnTrade(trade):
    print(trade)

@feed.feed.on(f"order.{pid}")
def OnOrder(order):
    print(order)


