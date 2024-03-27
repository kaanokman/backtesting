# -*- coding: utf-8 -*-
"""RMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yMaFwGRRgxiUCjFc-Bq3AbqRjKSJk--d

Import database
"""

pip install yfinance

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ticker = 'AAPL'

stock = yf.Ticker(ticker)
hist = stock.history(period="5y")
n = 15

long_days = 200
short_days = 50

rma_long_data = []
rma_short_data = []

closing_prices = hist[long_days:len(hist)]['Close']
dates = [datetime.date() for datetime in hist[long_days:len(hist)].index]

filtered_dates = dates[::n]

for day in range(long_days, len(hist)):
  rma_long_idx = day - long_days
  rma_short_idx = day - short_days
  rma_long = hist[rma_long_idx:day]['Close'].mean()
  rma_short = hist[rma_short_idx:day]['Close'].mean()

  rma_long_data.append(rma_long)
  rma_short_data.append(rma_short)

# Calculate the ADX
adx_period = 14
hist['TR'] = np.maximum.reduce([hist['High'] - hist['Low'], abs(hist['High'] - hist['Close'].shift()), abs(hist['Low'] - hist['Close'].shift())])
hist['DMplus'] = np.where((hist['High'] - hist['High'].shift()) > (hist['Low'].shift() - hist['Low']), np.maximum(hist['High'] - hist['High'].shift(), 0), 0)
hist['DMminus'] = np.where((hist['Low'].shift() - hist['Low']) > (hist['High'] - hist['High'].shift()), np.maximum(hist['Low'].shift() - hist['Low'], 0), 0)
hist['TRsmooth'] = hist['TR'].rolling(adx_period).mean()
hist['DMplus_smooth'] = hist['DMplus'].rolling(adx_period).mean()
hist['DMminus_smooth'] = hist['DMminus'].rolling(adx_period).mean()
hist['DIplus'] = (hist['DMplus_smooth'] / hist['TRsmooth']) * 100
hist['DIminus'] = (hist['DMminus_smooth'] / hist['TRsmooth']) * 100
hist['DX'] = np.abs(hist['DIplus'] - hist['DIminus']) / (hist['DIplus'] + hist['DIminus']) * 100
hist['ADX'] = hist['DX'].rolling(adx_period).mean()

adx = hist[long_days:len(hist)]['ADX']
x = range(len(dates))

# Find the buy and sell signals
signals = []
for i in range(1, len(rma_short_data)):
    if rma_short_data[i] >= rma_long_data[i] and rma_short_data[i-1] <= rma_long_data[i-1]:
        signals.append(('Buy', closing_prices[i]))
    if rma_short_data[i] <= rma_long_data[i] and rma_short_data[i-1] >= rma_long_data[i-1]:
        signals.append(('Sell', closing_prices[i]))
    else:
        signals.append(('None', None))

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(20, 10))

ax1.set_xticks(x[::n], filtered_dates, rotation='vertical')
ax2.set_xticks(x[::n], filtered_dates, rotation='vertical')

# Plot the RMA and closing price in the first subplot
ax1.plot(x, rma_long_data, color='darkslategrey', label=f'RMA {long_days}')
ax1.plot(x, rma_short_data, color='teal', label=f'RMA {short_days}')
ax1.plot(x, closing_prices, color='lightblue', label='Closing Price')

# Plot the ADX in the second subplot
ax2.plot(x, adx, color='purple', label=f'ADX ({adx_period})')

# Add a legend to the first subplot
ax1.legend()
ax2.legend()

# Plot the buy and sell signals
for signal in signals:
    if signal[0] == 'Buy':
        ax1.scatter(x[signals.index(signal)], round(signal[1], 2), color='green', marker='^', label='Buy Signal', zorder=10)
        ax1.text(x[signals.index(signal)], round(signal[1], 2), f'Buy: {round(signal[1], 2)}', ha='right', va='bottom', color='green', fontsize=10)
    elif signal[0] == 'Sell':
        ax1.scatter(x[signals.index(signal)], round(signal[1], 2), color='red', marker='v', label='Sell Signal', zorder=10)
        ax1.text(x[signals.index(signal)], round(signal[1], 2), f'Sell: {round(signal[1], 2)}', ha='right', va='top', color='red', fontsize=10)

# Add labels and a title to the plot
name = ticker
#name = stock.info['shortName']

ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{name} RMA Analysis')

ax2.set_xlabel('Date')
ax2.set_ylabel('ADX')
ax2.set_title(f'{name} ADX Analysis')

ax1.grid(True)
ax2.grid(True)
msft.news

# get option chain for specific expiration
opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts