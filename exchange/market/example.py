from lob.order_book import OrderBook

# Create a LOB object
lob = OrderBook()

########### Limit Orders #############

# Create some limit orders
someOrders = [{'type' : 'limit', 
            'side' : 'ask', 
            'qty' : 5, 
            'price' : 101,
            'tid' : 100},
            {'type' : 'limit', 
            'side' : 'ask', 
            'qty' : 5, 
            'price' : 103,
            'tid' : 101},
            {'type' : 'limit', 
            'side' : 'ask', 
            'qty' : 5, 
            'price' : 101,
            'tid' : 102},
            {'type' : 'limit', 
            'side' : 'ask', 
            'qty' : 5, 
            'price' : 101,
            'tid' : 103},
            {'type' : 'limit', 
            'side' : 'bid', 
            'qty' : 5, 
            'price' : 99,
            'tid' : 100},
            {'type' : 'limit', 
            'side' : 'bid', 
            'qty' : 5, 
            'price' : 98,
            'tid' : 101},
            {'type' : 'limit', 
            'side' : 'bid', 
            'qty' : 5, 
            'price' : 99,
            'tid' : 102},
            {'type' : 'limit', 
            'side' : 'bid', 
            'qty' : 5, 
            'price' : 97,
            'tid' : 103},
            ]

# Add orders to LOB
for order in someOrders:
    trades, idNum = lob.processOrder(order, False, False)

print(lob)

# Submitting a limit order that crosses the opposing best price will 
# result in a trade.
crossingLimitOrder = {'type' : 'market', 
                        'side' : 'bid', 
                        'qty' : 12, 
                        'price' : 103,
                        'tid' : 109}
trades, orderInBook = lob.processOrder(crossingLimitOrder, False, False)

print ("Trade occurs as incoming bid limit crosses best ask..")
for t in trades:
    print (t)
print (lob)
print(orderInBook)
print( lob.lastTick)
morrder = {'type' : 'limit', 
                        'side' : 'ask', 
                        'qty' : 4, 
                        'price' : 105.12313,
                        'tid' : 109}

                                                
trades, orderInBook = lob.processOrder(morrder, False, False)

print ("Trade -----------------")
print (trades)
print(orderInBook)
print (lob)
