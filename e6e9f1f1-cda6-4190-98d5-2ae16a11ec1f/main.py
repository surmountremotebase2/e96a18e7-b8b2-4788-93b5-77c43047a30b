from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, RSI
from surmount.logging import log
from datetime import datetime

class TradingStrategy(Strategy):
    def __init__(self):
        # High-growth tech tickers and stable dividend tickers
        self.tech_tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]
        self.dividend_tickers = ["JNJ", "PG", "KO", "PEP"]
        self.all_tickers = self.tech_tickers + self.dividend_tickers
        self.safety_net_enabled = False
        self.last_monthly_report = datetime.now()

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.all_tickers

    @property
    def data(self):
        # Use SMA for market condition assessment; no need to add as data list automatically includes OHLCV data
        return []

    def evaluate_market_condition(self, data):
        # Simple market condition based on SMA trends; more sophisticated metrics can be added
        market_condition = {"trend": "stable", "assessment": ""}

        sma_short = SMA("SPY", data, 10)  # Short-term SMA
        sma_long = SMA("SPY", data, 50)  # Long-term SMA

        if sma_short[-1] < sma_long[-1]:
            market_condition["trend"] = "downward"
            market_condition["assessment"] = "Market showing signs of downturn. Increasing stable dividend stock allocation."
        elif sma_short[-1] > sma_long[-1]:
            market_condition["trend"] = "upward"
            market_condition["assessment"] = "Market improving. Adjusting back to growth orientation."

        return market_condition

    def adjust_allocation_based_on_market(self, market_condition):
        allocation = {}

        if market_condition["trend"] == "downward":
            # Shift more towards dividend stocks
            for ticker in self.tech_tickers:
                allocation[ticker] = 0.40 / len(self.tech_tickers)
            for ticker in self.dividend_tickers:
                allocation[ticker] = 0.60 / len(self.dividend_tickers)
        elif market_condition["trend"] == "upward" or market_condition["trend"] == "stable":
            # Maintain or revert to normal allocation
            for ticker in self.tech_tickers:
                allocation[ticker] = 0.60 / len(self.tech_tickers)
            for ticker in self.dividend_tickers:
                allocation[ticker] = 0.40 / len(self.dividend_tickers)

        return allocation

    def run(self, data):
        current_date = datetime.now()

        # Evaluate current market condition
        market_condition = self.evaluate_market_condition(data)

        # Adjust allocation based on market condition
        allocation_dict = self.adjust_allocation_based_on_market(market_condition)

        # Generate monthly performance report
        if (current_date - self.last_monthly_report).days >= 30:
            log(f"Monthly report: {market_condition['assessment']}")
            self.last_monthly_report = current_date

        return TargetAllocation(allocation_dict)