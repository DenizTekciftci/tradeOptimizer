from mainclass import Stock
from switcher import optimizaion

# This example get the historical prices for the 'FB' ticker between start_date and end_date, and calculates the complete RSI-optimization
# All available optimization methods: 
# EMAS: EMA_weight, EMA_spans, EMA_complete
# RSI: RSI_length, RSI_bound, RSI_complete

# Initialization
ticker = 'FB'
start_date = "2018-01-01"
end_date = "2020-03-15"
date = start_date + "&" + end_date
trading_method = "RSI_complete"

# Create an instance of the Stock-class found in mainclass.py
stock = Stock(ticker, date, trading_method)

# Calls the optimization method 
optimized_parameters = optimizaion(stock)

# Prints the parameters
print(optimized_parameters)


