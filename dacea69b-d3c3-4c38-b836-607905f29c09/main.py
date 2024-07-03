from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]  # For this strategy, we're focusing on Apple Inc.

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Daily intervals for our MACD analysis

    def run(self, data):
        """
        Executes the trading strategy based on MACD signals.

        If the MACD line crosses above the signal line, an allocation is made (bullish signal).
        If the MACD line crosses below the signal line, the allocation is reduced or set to zero (bearish signal).
        """
        # Initialize allocation dict with no allocation
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        
        for ticker in self.tickers:
            # Compute MACD for the ticker
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            if macd_data is not None:
                # MACD and signal lines
                macd_line = macd_data["MACD"]
                signal_line = macd_data["signal"]
                
                # Check if we have at least two periods of data to compare crosses
                if len(macd_line) > 1 and len(signal_line) > 1:
                    latest_macd = macd_line[-1]
                    prev_macd = macd_line[-2]
                    latest_signal = signal_line[-1]
                    prev_signal = signal_line[-2]

                    # MACD line crosses above the signal line - bullish signal
                    if latest_macd > latest_signal and prev_macd <= prev_signal:
                        log(f"Bullish MACD crossover for {ticker}. Allocating funds.")
                        allocation_dict[ticker] = 0.5  # Allocate 50% of portfolio to this asset
                    # MACD line crosses below the signal line - bearish signal
                    elif latest_macd < latest_signal and prev_macd >= prev_signal:
                        log(f"Bearish MACD crossover for {ticker}. Reducing allocation.")
                        allocation_dict[ticker] = 0  # Reduce allocation to zero for this asset

        return TargetAllocation(allocation_dict)