import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import csv
import sys


# Year, Month, Day, Symbol, BUY or SELL, Number of Shares
def read_csv(filename):
    result = []
    with open(filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            result.append([dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16), float(row[3])])
    return result

def close_value(values):
    res = np.zeros((len(values), 1))
    for i in range(0, len(values)):
        res[i] = values[i][1]
    return res


def analyze_portfolio(rows):
    values = close_value(rows)
    
    # daily_returns
    na_normalized_price = values / values[0, :]
    returns = na_normalized_price.copy()
    tsu.returnize0(returns)    

    # std 
    std = np.std(returns)
    daily_ret = np.average(returns)
    sharpe = math.sqrt(252) * (daily_ret / std)

    daily_cum_ret = np.ones( (len(returns), 1) )
    for i in range (1, len(returns)):
        daily_cum_ret[i] = daily_cum_ret[i - 1] * (1 + returns[i])
    accum_ret = daily_cum_ret[len(daily_cum_ret) - 1][0]

    return std, daily_ret, sharpe, accum_ret


def analyze_stock(dt_start, dt_end, ls_symbols, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]

    na_rets = na_normalized_price.copy()
    tsu.returnize0(na_rets)

    # std 
    std = np.std(na_rets)
    daily_ret = np.average(na_rets)
    sharpe = math.sqrt(252) * (daily_ret / std)

    daily_cum_ret = np.ones( (len(na_rets), len(ls_symbols)) )

    for i in range (1, len(na_rets)):
        daily_cum_ret[i] = daily_cum_ret[i - 1] * (1 + na_rets[i])
    accum_ret = daily_cum_ret[len(daily_cum_ret) - 1][0]

    return std, daily_ret, sharpe, accum_ret


# python analyze.py values.csv $SPX
if __name__ == '__main__':
    values = read_csv(sys.argv[1])
    symbol = "$SPX" #sys.argv[2]

    std_port, daily_ret_port, sharpe_port, accum_ret_port = analyze_portfolio(values)
 
    start_date = values[0][0]
    end_date = values[len(values) - 1][0]
    std_sym, daily_ret_sym, sharpe_sym, accum_ret_sym = analyze_stock(
        start_date, end_date, [symbol], [1])

    print "The final value of the portfolio using the sample file is -- " + str(values[len(values) - 1])
    print ""
    print "Details of the Performance of the portfolio :"
    print ""
    print "Data Range : " + start_date.strftime('%Y-%m-%d') + " to  " + end_date.strftime('%Y-%m-%d')
    print ""
    print "Sharpe Ratio of Fund : " + str(sharpe_port)
    print "Sharpe Ratio of " + symbol + " : " + str(sharpe_sym)
    print ""
    print "Total Return of Fund : " + str(accum_ret_port)
    print "Total Return of " + symbol + " : " + str(accum_ret_sym)
    print ""
    print "Standard Deviation of Fund : " + str(std_port)
    print "Standard Deviation of Fund " + symbol + " : " + str(std_sym)
    print ""
    print "Average Daily Return of Fund : " + str(daily_ret_port)
    print "Average Daily Return of " + symbol + " : " + str(daily_ret_sym)
 