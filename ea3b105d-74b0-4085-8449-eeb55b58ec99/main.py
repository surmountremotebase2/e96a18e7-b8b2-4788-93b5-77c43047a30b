from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of tech tickers known for substantial market cap and liquidity
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Daily intervals for analysis

    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            rsi_data = RSI(ticker, data["ohlcv"], length=14)

            if not macd_data or not rsi_data:
                log(f"Insufficient data for {ticker}")
                continue

            # Get the last MACD and signal values
            macd = macd_data["MACD"][-1]
            signal = macd_data["signal"][-1]
            rsi = rsi_data[-1]

            # Initial allocation is cautious, zeroing until a buy signal is confirmed
            allocation_dict[ticker] = 0

            # Buying criteria: MACD crosses above signal line and not overbought (RSI < 70)
            if macd > signal and rsi < 70:
                log(f"Buying signal for {ticker}")
                allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally distribute allocation
            
            # Implicit else: Do not allocate capital to this asset due to lack of signal or overbought condition

        return TargetAllocation(allocation_dict)