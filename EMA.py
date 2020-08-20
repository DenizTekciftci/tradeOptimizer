# Optimizes the weightings and the bounds
def complete_optimization(data, EMA_short_length, EMA_long_length, partitions, max_len_short, max_len_long, min_len_short=None, min_len_long=None):
    # Initialize
    profit, weight, prev_weight, prev_span_short, prev_span_long = -1,-1,-1,-1,-1
    unstable = (weight != prev_weight or EMA_short_length != prev_span_short or EMA_long_length != prev_span_long)

    while unstable:
        prev_span_long = EMA_long_length
        prev_span_short = EMA_short_length
        prev_weight = weight

        weight, profit = weight_optimization(data, EMA_short_length, EMA_long_length, partitions)
        EMA_short_length, EMA_long_length, profit = spans_optimization(data, weight, max_len_short, max_len_long, min_len_short, min_len_short)

        unstable = (weight != prev_weight or EMA_short_length != prev_span_short or EMA_long_length != prev_span_long)

    return {"weight" : weight, "EMA_short_length" : EMA_short_length, "EMA_long_length": EMA_long_length, "profit":profit}

# Optimizes the weighting used for calculating the EMA
def weight_optimization(data, EMA_short_length, EMA_long_length, partitions):
    # Initialize
    best_weight = -1, -1
    balance, change, num_of_purchases = 0,0,0

    for x in range(1,partitions):
        weight = x / partitions
        tw_short = total_weight(weight, EMA_short_length)
        tw_long = total_weight(weight, EMA_long_length)

        EMA_short = initialize(data, weight, tw_short, EMA_long_length, EMA_short_length)
        EMA_long = initialize(data, weight, tw_long, EMA_long_length)
        balance, change, num_of_purchases = trading(data, weight, EMA_short, EMA_long, tw_short, tw_long, EMA_short_length, EMA_long_length)
        
        if balance > max_profit:
            best_weight = weight
            max_profit = balance

    return best_weight, max_profit

# Optimizes the spans for the EMAs
def spans_optimization(data, weight, max_len_short, max_len_long, min_len_short=None, min_len_long=None):
    # Initialize
    best_span_short = -1, -1
    balance, change = 0, 0
    
    if min_len_short == None:
        min_len_short = 5
    else:
        min_len_short = min_len_short
        
    if min_len_long == None:
        min_len_long = 10   
    else:
        min_len_long = min_len_long

    for EMA_long_length in range(min_len_long, max_len_long, 2):
        if max_len_short >= EMA_long_length:
            max_len_short_dyn = EMA_long_length//2 + 1
        else:
            max_len_short_dyn = max_len_short

        for EMA_short_length in range(min_len_short, max_len_short_dyn, 2):

            tw_short = total_weight(weight, EMA_short_length)
            tw_long = total_weight(weight, EMA_long_length)

            EMA_short = initialize(data, weight, tw_short, EMA_long_length, EMA_short_length)
            EMA_long = initialize(data, weight, tw_long, EMA_long_length)

            balance, change, num_of_purchases = trading(data, weight, EMA_short, EMA_long, tw_short, tw_long, EMA_short_length, EMA_long_length)
            
            if balance > max_profit:
                best_span_short = EMA_short_length
                best_span_long = EMA_long_length
                max_profit = balance

    return best_span_short, best_span_long, max_profit


# Simulates the trading
def trading(data, weight, EMA_short, EMA_long, tw_short, tw_long, EMA_short_length, EMA_long_length):
    # Initialize
    min_weight_short = weight ** EMA_short_length
    min_weight_long = weight ** EMA_long_length

    bull = True
    if (EMA_long > EMA_short):
        bull = False

    balance = 0
    num_of_purchases = 0

    for i in range(EMA_long_length, len(data)):
        EMA_short = EMA_short * weight + (data[i]["close"] - data[i - EMA_short_length]["close"]*min_weight_short)/tw_short
        EMA_long = EMA_long * weight + (data[i]["close"] - data[i- EMA_long_length]["close"]*min_weight_long)/tw_long

        if (not bull) and (EMA_short >= EMA_long):
            num_of_purchases += 1
            bull = True
            balance -= data[i]["close"]

        if bull and (EMA_short < EMA_long):
            bull = False
            if balance != 0:
                balance += data[i]["close"]

    if bull and num_of_purchases != 0:
        balance += data[len(data) -1]["close"]

    change = data[len(data) -1]["close"] - data[0]["close"]
    return balance, change, num_of_purchases

# Calculates the total weight
def total_weight(weight, i):
    tw = 0
    multiplier = 1

    for _ in range(i):
        tw += multiplier
        multiplier *= weight
    
    return tw


# Initializes the EMA queues
def initialize(data, weight, total_weight, EMA_long_length, EMA_short_length=None):
    EMA = 0
    multiplier = 1
    if EMA_short_length == None:
        Range = range(EMA_long_length)
    else:
        Range= range(EMA_long_length - EMA_short_length, EMA_long_length)

    for i in reversed(Range):
        EMA += data[i]["close"] * multiplier
        multiplier *= weight
    
    return EMA / total_weight