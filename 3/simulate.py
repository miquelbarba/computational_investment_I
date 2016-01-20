import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def simulate(dt_start, dt_end, ls_symbols, allocations):
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

    daily_cum_ret = np.ones( (len(na_rets), len(ls_symbols)) )

    for i in range (1, len(na_rets)):
        daily_cum_ret[i] = daily_cum_ret[i - 1] * (1 + na_rets[i])
    accum_ret = daily_cum_ret[len(daily_cum_ret) - 1]

    cum_ret = 0
    for index, item in enumerate(allocations):
        cum_ret += item * accum_ret[index]

    return cum_ret

ls_symbols = ["AAPL", "GLD", "GOOG", "XOM"]
allocations = [0.4, 0.4, 0.0, 0.2]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
cum_ret = simulate(dt_start, dt_end, ls_symbols, allocations)
print cum_ret