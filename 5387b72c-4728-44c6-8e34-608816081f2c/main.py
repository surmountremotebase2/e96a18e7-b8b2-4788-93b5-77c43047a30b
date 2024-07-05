from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InstitutionalOwnership

class TradingStrategy(Strategy):
    def __init__(self):
        # FAANG tickers, note that Facebook is now under Meta Platforms, Inc. with the ticker 'META'
        self.tickers = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        
        # Start with an equal distribution across FAANG stocks
        initial_allocation = 1.0 / len(self.tickers)
        
        for ticker in self.tickers:
            # Default allocation for each stock
            allocation_dict[ticker] = initial_allocation
            institutional_data_key = ("institutional_ownership", ticker)
            
            # Check if we have institutional ownership data for the current ticker
            if institutional_data_key in data and len(data[institutional_data_key]) > 0:
                # We look at the most recent data point
                most_recent_data = data[institutional_data_key][-1]
                # Example logic: if the ownership percent has increased from the last reported value, we increase our allocation
                if most_recent_data["ownershipPercentChange"] > 0:
                    # Increase our allocation by a certain factor; ensuring it doesn't go above a maximum value
                    allocation_dict[ticker] = min(initial_allocation + 0.05, 0.3)  # Capped at 30% allocation, for example
                else:
                    # Decrease our stake if the ownership percent has decreased, ensuring it doesn't go below a minimum value
                    allocation_dict[ticker] = max(initial_allocation - 0.05, 0.05)  # Ensured not to go below 5% allocation
                
            else:
                # If no data available, stick to the initial allocation (equal distribution logic)
                allocation_dict[ticker] = initial_allocation

        # Return the final allocation across the FAANG stocks
        return TargetAllocation(allocation_dict)