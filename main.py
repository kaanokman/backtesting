# imports
import yfinance as yf
import matplotlib.pyplot as plt

# select stock
ticker = 'AAPL'

# select backtesting period
period = "5y"

stock = yf.Ticker(ticker)
hist = stock.history(period)

# rolling moving average details
long_days = 200
short_days = 50

rma_long_data = []
rma_short_data = []

closing_prices = hist[long_days:len(hist)]['Close']
dates = [datetime.date() for datetime in hist[long_days:len(hist)].index]

# select number of days to skip for plot
n = 30

filtered_dates = dates[::n]

for day in range(long_days, len(hist)):
  rma_long_idx = day - long_days
  rma_short_idx = day - short_days
  rma_long = hist[rma_long_idx:day]['Close'].mean()
  rma_short = hist[rma_short_idx:day]['Close'].mean()

  rma_long_data.append(rma_long)
  rma_short_data.append(rma_short)

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

# create a figure and set ticks
fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(14, 7))
ax1.set_xticks(x[::n], filtered_dates, rotation='vertical')

# plot the RMA and closing price in the first subplot and add legend
ax1.plot(x, rma_long_data, color='darkslategrey', label=f'RMA {long_days}')
ax1.plot(x, rma_short_data, color='teal', label=f'RMA {short_days}')
ax1.plot(x, closing_prices, color='lightblue', label='Closing Price')
ax1.legend()

# plot the buy and sell signals
for signal in signals:
    if signal[0] == 'Buy':
        ax1.scatter(x[signals.index(signal)], round(signal[1], 2), color='green', marker='^', label='Buy Signal', zorder=10)
        ax1.text(x[signals.index(signal)], round(signal[1], 2), f'Buy: {round(signal[1], 2)}', ha='right', va='bottom', color='green', fontsize=10)
    elif signal[0] == 'Sell':
        ax1.scatter(x[signals.index(signal)], round(signal[1], 2), color='red', marker='v', label='Sell Signal', zorder=10)
        ax1.text(x[signals.index(signal)], round(signal[1], 2), f'Sell: {round(signal[1], 2)}', ha='right', va='top', color='red', fontsize=10)

# add labels and a title to the plot
name = ticker
ax1.set_xlabel('Date')
ax1.set_ylabel('Price')
ax1.set_title(f'{name} RMA Analysis')
ax1.grid(True)

# show plot
plt.show()
