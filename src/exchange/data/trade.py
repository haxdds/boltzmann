from typing import Dict

class Trade:

    def __init__(self, timestamp: float, price: float, qty: float, participant1: Dict, participant2: Dict):
        self.timestamp = timestamp
        self.price = price
        self.qty = qty
        self.party_one_pid = participant1['tid']
        self.party_two_pid = participant2 ['tid']
        self.party_one_side = participant1['side']
        self.party_two_side = participant2['side']
        self.party_one_order_id = participant1['idNum']
        self.party_two_order_id = participant2['idNum']

    @staticmethod
    def parse_trades(self, trades):
        parsed = []
        for trade in trades:
            parsed.append(self.parse_trade(trade))
        return parsed

    @staticmethod
    def parse_trade(self, trade):
        party1Dict = {'tid': trade['party1'][0], 'side': trade['party1'][1], 'idNum': trade['party1'][2]}
        party2Dict = {'tid': trade['party2'][0], 'side': trade['party2'][1], 'idNum': trade['party2'][2]}
        return Trade(trade['timestamp'], trade['price'], trade['qty'], party1Dict, party2Dict)
