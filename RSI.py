from EMA import total_weight
from collections import deque

# LBB = Lower bound buy
# UBB = Upper bound buy
# LBS = Lower bound sell
# UBS = Upper bound sell

# Optimizes both the length and bound
def complete_optimization(data, length, LBB, UBB, LBS, UBS):
    # Initialize data
    PREV_length, PREV_LBB, PREV_UBB, PREV_LBS, PREV_UBS = -1,-1,-1,-1,-1
    UNSTABLE = (length != PREV_length or LBB != PREV_LBB or UBB != PREV_UBB or PREV_LBS != LBS or PREV_UBS != UBS)

    while UNSTABLE:
        PREV_length = length
        PREV_LBB = LBB
        PREV_UBB = UBB
        PREV_LBS = LBS
        PREV_UBS = UBS

        length, profit = length_optimization(data, LBB, UBB, LBS, UBS)
        LBB, UBB, LBS, UBS, profit = bound_optimization(data, length)

        UNSTABLE = (length != PREV_length or LBB != PREV_LBB or UBB != PREV_UBB or PREV_LBS != LBS or PREV_UBS != UBS)
    
    return {"profit": profit, "length": length, "LBB": LBB, "UBB" : UBB, "LBS" : LBS, "UBS": UBS}

# Optimizes the length 
def length_optimization(data, LBB, UBB, LBS, UBS): #length is temporary
    # Initialize data
    MAX_profit, OPT_length = -1, -1

    for length in range(7, 25):
        RSI, gains, loss = initialize(data, length)
        balance, num_of_trades = trading(data, RSI, gains, loss, length, LBB, UBB, LBS, UBS)

        if balance > MAX_profit:
            MAX_profit = balance
            OPT_length = length
    
    return OPT_length, MAX_profit

# Optimizes the bounds
def bound_optimization(data, length):
    MAX_profit, OPT_LBB, OPT_UBB, OPT_LBS, OPT_UBS = -1, -1, -1, -1, -1
    LBB_start = 30
    UBB_start = 70
    LBS_start = 45
    UBS_start = 55
    for i in range(16):
        for j in range(16):
            LBB = LBB_start - i
            UBB = UBB_start + i
            LBS = LBS_start - j
            UBS = UBS_start + j
            RSI, gains, loss = initialize(data, length)
            profit, num_of_trades = trading(data, RSI, gains, loss, length, LBB, UBB, LBS, UBS)

            if profit > MAX_profit:
                MAX_profit = profit
                OPT_LBB = LBB
                OPT_UBB = UBB
                OPT_LBS = LBS
                OPT_UBS = UBS

    return OPT_LBB,  OPT_UBB, OPT_LBS, OPT_UBS,  MAX_profit

# Initializes the the RSI queue
def initialize(data, length):
    gains, loss = deque(maxlen=length), deque(maxlen=length)
    for i in range(1, length+1):
        change = data[i]["close"] - data[i-1]["close"]
        if change > 0:
            gains.appendleft(change)
            loss.appendleft(0)
        else:
            gains.appendleft(0)
            loss.appendleft(change)

    avg_up = RMA(gains, 1)
    avg_down = RMA(loss, 1) + 0.00001
    RS = avg_up / (-1 * avg_down)

    RSI = 100 - (100 / (1 + RS))
    return RSI, gains, loss

# RMA function
def RMA(data, weight):
    sum = 0
    for i in range(len(data)):
        alpha = 1/(i + 1)
        sum = alpha * data[i] + (1 - alpha) * sum
    return sum

# Calculates the RSI with the next element
def calc_next(data, gains, loss, next):
    change = data[next]["close"] - data[next - 1]["close"]
    if change > 0:
        gains.appendleft(change)
        loss.appendleft(0)
    else:
        gains.appendleft(0)
        loss.appendleft(change)

    avg_up = RMA(gains, 1)
    avg_down = RMA(loss, 1) + 0.00001
    RS = avg_up / (-1 * avg_down) 
    RSI = 100 - (100 / (1 + RS))

    return RSI, gains, loss

# Simulates the trading
def trading(data, RSI, gains, loss, length, LBB, UBB, LBS, UBS):
    position = None
    short = -1
    long = 1
    purchases, profit = 0, 0
    for i in range(length, len(data)):

        if position == None:
            if RSI < LBB:
                position = long
                profit -= data[i]["close"]
                purchases += 1

            if RSI > UBB:
                position = short
                profit += data[i]["close"]
                purchases += 1

        if position == long and RSI > UBS:
            profit += data[i]["close"]
            position = None

        if position == short and RSI < LBS:
            profit -= data[i]["close"]
            position = None

        RSI, gains, loss = calc_next(data, gains, loss, i)

    if position == long:
        profit += data[len(data) - 1]["close"]
    elif position == short:
        profit -= data[len(data) - 1]["close"]
    
    return profit, purchases