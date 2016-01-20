import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from decimal import *


def simulate(dt_start, dt_end, ls_symbols, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]
    na_normalized_price_alloc = na_normalized_price * allocations

    sum_daily = np.zeros( len(na_normalized_price_alloc) )
    for index, item in enumerate(na_normalized_price_alloc):
        for value in item:
            sum_daily[index] += value

    na_rets = sum_daily.copy()
    tsu.returnize0(na_rets)
        
    daily_cum_ret = np.ones( len(na_rets) )
    for i in range (1, len(na_rets)):
        daily_cum_ret[i] = daily_cum_ret[i - 1] * (1 + na_rets[i])
    cum_ret = daily_cum_ret[len(daily_cum_ret) - 1]

    vol = np.std(na_rets)
    daily_ret = np.average(na_rets)
    sharpe = math.sqrt(252) * (daily_ret/vol)

    return vol, daily_ret, sharpe, cum_ret


def optimize(dt_start, dt_end, ls_symbols):
    num_portfolios = 0
    max_sharpe = 0
    max_allocation = None
    len_symbols = len(ls_symbols)
    for i in np.arange(0, 11, 1):
        for j in np.arange(0, 11, 1):
            for k in np.arange(0, 11, 1):
                for l in np.arange(0, 11, 1):
                    if i + j + k + l == 10:
                        num_portfolios += 1
                        allocations = [i/10.0, j/10.0, k/10.0, l/10.0]
                        print "num_portfolios: ", num_portfolios, " i: ", i, " j: ", j, " k: ", k, " l: ", l, " sum: ", (i + j + k + l)
                        vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, allocations)
                        print "allocation", allocations, "  sharpe ", sharpe
                        if sharpe > max_sharpe:
                            max_sharpe = sharpe
                            max_allocation = allocations

    return max_allocation, max_sharpe

 

ls_symbols = ['BRCM', 'TXN', 'AMD', 'ADI']
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)

max_allocation, max_sharpe = optimize(dt_start, dt_end, ls_symbols)

print "RESULT, allocation: ", max_allocation
print "RESULT, max_sharpe: ", max_sharpe

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, max_allocation)

print "Sharpe Ratio: ", sharpe
print "Volatility (stdev of daily returns): ", vol
print "Average Daily Return: ", daily_ret
print "Cumulative Return: ", cum_r


"""
ls_symbols = ['C', 'GS', 'IBM', 'HNZ'] 
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)

max_allocation, max_sharpe = optimize(dt_start, dt_end, ls_symbols)

print "RESULT, allocation: ", max_allocation
print "RESULT, max_sharpe: ", max_sharpe

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, max_allocation)

print "Sharpe Ratio: ", sharpe
print "Volatility (stdev of daily returns): ", vol
print "Average Daily Return: ", daily_ret
print "Cumulative Return: ", cum_ret

RESULT, allocation:  [0.20000000000000001, 0.0, 0.0, 0.80000000000000004]
RESULT, max_sharpe:  1.36716552762
Scratch Directory:  /var/folders/rr/j1jkg4js22536g0xq_9b4q280000gn/T/QSScratch
Data Directory:  /Users/miquel/QSTK-0.2.5/QSTK/qstkutil/../QSData
Sharpe Ratio:  1.36716552762
Volatility (stdev of daily returns):  0.0104738868269
Average Daily Return:  0.0009020460





ls_symbols = ["AAPL", "GLD", "GOOG", "XOM"]
allocations = [0.4, 0.4, 0.0, 0.2]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)

max_allocation, max_sharpe = optimize(dt_start, dt_end, ls_symbols)

print "RESULT, allocation: ", max_allocation
print "RESULT, max_sharpe: ", max_sharpe

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, max_allocation)

print "Sharpe Ratio: ", sharpe
print "Volatility (stdev of daily returns): ", vol
print "Average Daily Return: ", daily_ret
print "Cumulative Return: ", cum_ret

print "---------------------------------------------"

dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']

max_allocation, max_sharpe = optimize(dt_start, dt_end, ls_symbols)

print "RESULT, allocation: ", max_allocation
print "RESULT, max_sharpe: ", max_sharpe

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, max_allocation)

print "Sharpe Ratio: ", sharpe
print "Volatility (stdev of daily returns): ", vol
print "Average Daily Return: ", daily_ret
print "Cumulative Return: ", cum_ret




dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)
ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
allocations = [0.0, 0.0, 0.0, 1.0]

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, ls_symbols, allocations)
print "Sharpe Ratio: ", sharpe
print sharpe
print "Volatility (stdev of daily returns): ", vol
print vol
print "Average Daily Return: ", daily_ret
print daily_ret
print "Cumulative Return: ", cum_ret
print cum_ret
"""