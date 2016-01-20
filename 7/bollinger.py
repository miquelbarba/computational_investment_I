import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas
from pylab import *

#
# Prepare to read the data
#
symbols = ["MSFT"]
startday = dt.datetime(2010,4,1)
endday = dt.datetime(2010,5,22)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

dataobj = da.DataAccess('Yahoo')
voldata = dataobj.get_data(timestamps, symbols, "volume")
adjcloses = dataobj.get_data(timestamps, symbols, "close")
actualclose = dataobj.get_data(timestamps, symbols, "actual_close")

adjcloses = adjcloses.fillna()
adjcloses = adjcloses.fillna(method='backfill')

means = pandas.rolling_mean(adjcloses,20,min_periods=20)
std = pandas.rolling_std(adjcloses, 20, min_periods=20)

bollinger_val = (adjcloses - means) / std

print bollinger_val['MSFT']

