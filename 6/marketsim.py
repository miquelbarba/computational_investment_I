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
            result.append([dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16), row[3].strip(), row[4].strip(), int(row[5])])
    return result

def write_csv(filename, array):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in array:
            writer.writerow(row)

def sort_by_date(orders):
    return sorted(orders, key=lambda x: x[0])

def adjusted_close(symbol, date):
    dataobj = da.DataAccess('Yahoo')
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data([date], [symbol], keys)
    d_data = dict(zip(keys, ldf_data))
    return d_data['close'].values[0][0]

def get_order_index(date, orders):
    i = 0
    found = False
    size = len(orders)
    while i < size and not found:
        found = date.date() == orders[i][0].date()
        if not found: 
            i += 1
    return i if found else None

def get_symbol_index_from_portfolio(portfolio, symbol):
    i = 0
    found = False
    size = len(portfolio)
    while i < size and not found:
        found = portfolio[i][0] == symbol
        if not found:
            i += 1
    return i if found else None

def add_portfolio(portfolio, symbol, num_shares):
    index = get_symbol_index_from_portfolio(portfolio, symbol)
    if index == None:
        portfolio.append([symbol, num_shares])
    else:
        portfolio[index][1] += num_shares

def remove_portfolio(portfolio, symbol, num_shares):
    index = get_symbol_index_from_portfolio(portfolio, symbol)
    if index == None:
        portfolio.append([symbol, -num_shares])
    else:
        portfolio[index][1] -= num_shares
        if portfolio[index][1] == 0:
            portfolio.pop(index)

def process_order(date, order, portfolio, current_cash):
    num_shares = order[3]
    symbol = order[1]
    price = adjusted_close(symbol, date)
    amount = price * num_shares
    if order[2].lower() == 'BUY'.lower():
        add_portfolio(portfolio, symbol, num_shares)
        return current_cash - amount
    else:
        remove_portfolio(portfolio, symbol, num_shares)
        return current_cash + amount

def process_orders(date, orders, portfolio, current_cash):
    size = len(orders)
    index_order = get_order_index(date, orders)

    end = index_order == None
    cash = current_cash
    while index_order < size and not end:
        order = orders[index_order]
        cash = process_order(date, order, portfolio, cash)
        index_order += 1
        end = index_order >= size or orders[index_order][0].date() != date.date()
    return cash

def calculate_value_equities(date, portfolio):
    value = 0
    for stock in portfolio:
        value += adjusted_close(stock[0], date) * stock[1]
    return value

def calculate(orders, initial_cash):
    dt_start = orders[0][0]
    dt_end = orders[len(orders) - 1][0]
    timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    res = []
    portfolio = []
    cash = initial_cash
    for date in timestamps:
        cash = process_orders(date, orders, portfolio, cash)
        total = cash + calculate_value_equities(date, portfolio)
        res.append([date.year, date.month, date.day, total])
    return res


# python marketsim.py 1000000 orders.csv values.csv
if __name__ == '__main__':
    unsorted_orders = read_csv(sys.argv[2])
    orders = sort_by_date(unsorted_orders)
    initial_cash = int(sys.argv[1])
    res = calculate(orders, initial_cash)
    write_csv(sys.argv[3], res)

