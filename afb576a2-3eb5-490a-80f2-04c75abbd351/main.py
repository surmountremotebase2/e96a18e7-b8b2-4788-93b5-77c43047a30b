from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA  # Assuming these might be useful for trend analysis
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["FB", "AMZN", "NFLX", "GOOGL"]  # FANG stocks

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Example logic for determining if a stock is "gaining"
            # Here, a simple mock is an increase in the simple moving average (SMA)
            # Note: In a real scenario, more sophisticated analysis would be required
            try:
                closing_prices = [data["ohlcv"][-i][ticker]["close"] for i in range(1, 6)]  # Last 5 days' close prices
                current_sma = sum(closing_prices) / len(closing_prices)
                previous_sma = sum(closing_prices[1:]) / (len(closing_prices)-1)
                
                if current_sma > previous_sma:  # Assuming gaining if current SMA is greater than previous
                    allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally divide allocation among gaining FANG stocks
                else:
                    allocation_dict[ticker] = 0  # Do not allocate to non-gaining stocks
            except Exception as e:
                log(f"Error processing {ticker}: {e}")
                allocation_dict[ticker] = 0  # Failsafe: do not allocate if there's an issue fetching data
            
        # Normalize allocation_dict to ensure sum of allocations does not exceed 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: weight / total_allocation for ticker, weight in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)