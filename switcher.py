import EMA as EMA
import RSI as RSI

def EMA_weight(stock):
    EMA_short_length = 20
    EMA_long_length = 100
    partitions = 10

    return EMA.weight_optimization(stock.historical_prices, EMA_short_length, EMA_long_length, partitions)

def EMA_spans(stock):
    print("we here")
    weight = 0.4
    max_len_long = 200
    max_len_short = 50
    min_len_short= 10
    min_len_long= 50
    
    return EMA.spans_optimization(stock.historical_prices, weight, max_len_short, max_len_long, min_len_short, min_len_long)

def EMA_complete(stock):
    #Idea is, run quick weight optimization, then run it through the spans optimization
    #Then back and forward until nothing changes

    #Information for first weight optimization
    EMA_short_length = 20
    EMA_long_length = 40
    partitions = 100

    #Information for spans optimization
    max_len_short = 50
    max_len_long = 100
    min_len_short= None
    # min_len_long= 10

    return EMA.complete_optimization(stock.historical_prices, EMA_short_length, EMA_long_length, partitions, max_len_short, max_len_long, min_len_short)

def RSI_length(stock):
    LBB = 30
    UBB = 70
    LBS = 45
    UBS = 55

    return RSI.length_optimization(stock.historical_prices, LBB, UBB, LBS, UBS)

def RSI_bound(stock):
    length = 14

    return RSI.bound_optimization(stock.historical_prices, length)

def RSI_complete(stock):
    length = 14
    LBB = 30
    UBB = 70
    LBS = 45
    UBS = 55

    return RSI.complete_optimization(stock.historical_prices, length, LBB, UBB, LBS, UBS)

def optimizaion(stock):
    switcher = {
        "EMA_weight": EMA_weight,
        "EMA_spans": EMA_spans,
        "EMA_complete": EMA_complete,

        "RSI_length": RSI_length,
        "RSI_bound": RSI_bound,
        "RSI_complete": RSI_complete
    }
    function = switcher.get(stock.optimization_method, "Eksisterer ikke")
    return function(stock)

