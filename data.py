import requests
# Calls data-API for the ticker and wanted type of data
def getData(tickers, data_type, date_or_period, key=None):
    response = []
    for ticker in tickers:
        url = "https://financialmodelingprep.com/api/v3/"+ data_type + "/" + ticker + "?apikey=573fd8f31cf7a1f77335651feaba2577&" +  date_or_period
        res = requests.get(url)
        if(key==None):
            response.append(res.json())
        else:
            response.append(res.json()[key])
    return response

# Validates whether the API has data in the wanted fields
def validateData(financial_ratios, key_metrics):
    fr = {"profitabilityIndicatorRatios" : ["netProfitMargin", "returnOnEquity"], "liquidityMeasurementRatios" : ["daysOfSalesOutstanding"],
    "cashFlowIndicatorRatios": ["payoutRatio"]
    }
    km = ["Market Cap", "Net Debt to EBITDA"]

    for key in fr:
        for ratio in fr[key]:
            if len(financial_ratios[key][ratio])==0:
                return False
    
    for metric in km:
        if len(key_metrics[metric])==0:
            return False

    return True
    
                
