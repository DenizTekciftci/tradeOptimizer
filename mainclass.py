from data import getData

class Stock:
    def __init__(self, ticker, date, optimization_method):
        self.ticker = ticker
        self.optimization_method = optimization_method

        data_type = "historical-price-full"
        key = "historical"
        self.historical_prices = getData([self.ticker], data_type, date, key)[0]

        data_type = "company-key-metrics"
        period = "period=quarter"
        self.key_metrics = getData([self.ticker], data_type, period)[0]