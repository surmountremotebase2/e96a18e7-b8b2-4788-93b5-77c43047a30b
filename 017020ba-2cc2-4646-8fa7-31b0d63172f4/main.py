from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.asset = "AAPL"

    @property
    def assets(self):
        return [self.asset]

    @property
    def interval(self):
        return "1day"

    @property
    def data(self):
        return []

    def run(self, data):
        # EMA settings
        short_term_period = 12
        long_term_period = 26

        # RSI settings
        rsi_period = 14
        rsi_buy_threshold = 50  # RSI level indicating momentum but not overbought
        rsi_sell_threshold = 45  # RSI level to suggest a potential downturn

        allocation_dict = {self.asset: 0}  # Default to no position
        ohlcv_data = data["ohlcv"]
        
        if len(ohlcv_data) > long_term_period:
            short_term_ema = EMA(self.asset, ohlcv_data, length=short_term_period)
            long_term_ema = EMA(self.asset, ohlcv_suohlcv_datadata, length=long_term_period)
            rsi = RSI(self.asset, ohlcv_data, length=rsi_period)
            
            # Check for buy signals
            if (short_term_ema[-1] > long_term_ema[-1]) and (rsi[-1] > rsi_buy_threshold):
                log("Buy signal detected")
                allocation_dict[self.asset] = 1  # Full allocation to AAPL
            
            # Check for sell signals
            elif (short_term_ema[-1] < long_term_ema[-1]) or (rsi[-1] < rsi_sell_threshold):
                log("Sell signal detected")
                allocation_dict[self.asset] = 0  # Exiting position
            
            # Otherwise, maintain current position
            else:
                log("No clear signal, maintaining current position")

        return TargetInventory(allocation_dict)