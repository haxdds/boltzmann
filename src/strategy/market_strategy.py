from abc import ABC, abstractmethod
from enum import Enum

class StrategyType(Enum):
    MOMENTUM = 1,
    LONG_ONLY = 2,
    SHORT_ONLY = 3,
    MARKET_MAKING = 4,
    LONG_TERM_INVESTMENT = 5, # buy and hold / short and hold
    SHORT_TERM_INVESTMENT = 6,
    VOLATILITY = 7,
    


class MarketStrategy(ABC):

    def __init__(self, name: str, time_scale: float, type: StrategyType):
        self.name = name
        self.time_scale = time_scale
        self.type = type

    @abstractmethod
    def compute_action(self, market_data, portfolio):
        pass
