from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, SMA, MACD
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership, InsiderTrading, SocialSentiment, FinancialStatement

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to trade
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
        # Define the data required for the strategy
        self.data_list = [InstitutionalOwnership(ticker) for ticker in self.tickers]
        self.data_list += [InsiderTrading(ticker) for ticker in self.tickers]
        self.data_list += [SocialSentiment(ticker) for ticker in self.tickers]
        self.data_list += [FinancialStatement(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # Use daily data for this strategy
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Initialize the allocation to 0
            allocation_dict[ticker] = 0.0
            
            # Technical analysis conditions
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            rsi_data = RSI(ticker, data["ohlcv"], length=14)
            sma_short = SMA(ticker, data["ohlcv"], length=50)
            sma_long = SMA(ticker, data["ohlcv"], length=200)
            
            if len(rsi_data) > 0 and len(sma_short) > 0 and len(sma_long) > 0:
                # Condition for "buy" signal (simplified for illustration)
                if macd_data["MACD"][-1] > macd_data["signal"][-1] and rsi_data[-1] < 70 \
                   and sma_short[-1] > sma_long[-1]:
                    allocation_dict[ticker] = 0.2  # Allocate 20% to this ticker
                
                # Condition for "sell" signal (simplified for illustration)
                elif macd_data["MACD"][-1] < macd_data["signal"][-1] or rsia_data[-1] > 70:
                    allocation_dict[ticker] = 0  # Sell off this ticker
                
                # Adjust based on sentiment (simplified for illustration)
                sentiment_data = data[("social_sentiment", ticker)]
                if sentiment_data and len(sentiment_data) > 0 and sentiment_data[-1]['stocktwitsSentiment'] > 0.6:
                    allocation_dict[ticker] += 0.05  # Increase allocation by 5%
                # Ensure allocation does not exceed 100%
                if allocation_dict[ticker] > 1.0:
                    allocation_dict[ticker] = 1.0

        return TargetAllocation(allocation_dict)