from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tech stocks or ETFs to track.
        self.tickers = ["QQQ", "AAPL"]
        self.assets_data = [Asset(i) for i in self.tickers]
        
    @property
    def interval(self):
        return "1day"  # Daily interval for analysis
        
    @property
    def assets(self):
        return self.tickers
    
    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ohlcv = data["ohlcv"]
            
            # Calculate RSI to detect overbought/oversold conditions
            rsi = RSI(ticker, ohlcv, length=14)  # Standard 14-day period
            
            # Calculate the Short-term (20-day) and Long-term (50-day) SMAs
            sma_short = SMA(ticker, ohlcv, length=20)
            sma_long = SMA(ticker, ohlcv, length=50)
            
            if not rsi or not sma_short or not sma_long:
                continue  # Skip this cycle if the data isn't complete
                
            # Sell condition: If the last RSI is > 70 (overbought), or current price is below long-term SMA (downtrend)
            if rsi[-1] > 70 or ohlcv[-1][ticker]["close"] < sma_long[-1]:
                allocation_dict[ticker] = 0  # Move to 0% allocation for this ticker
                
            # Buy condition: If the last RSI is < 30 (oversold), or short-term SMA crosses above long-term SMA (uptrend)
            elif rsi[-1] < 30 or (sma_short[-1] > sma_long[-1] and sma_short[-2] < sma_long[-2]):
                allocation_dict[ticker] = 0.5  # Allocate 50% of portfolio to this ticker, considering risk management
                
            # Hold/Neutral condition
            else:
                allocation_dict[ticker] = 0.25  # Hold a moderate position as a baseline approach
                
        # Ensure the allocation does not exceed 100%
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            # Scale down allocations to fit the budget
            allocation_dict = {ticker: alloc / total_allocation for ticker, alloc in allocation_dict.items()}
            
        return TargetAllocation(allocation_dict)