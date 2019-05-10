from __future__ import division

import pandas
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

def addBar(xpos, quote, barWidth, colorUpper, colorLower, alpha):
    date, o, h, l, c = quote
    if o >= c:
        color = colorLower
        barHeight = o-c
        lowestBarPosition = c
    else:
        color = colorUpper
        barHeight = c-o
        lowestBarPosition = o

    line = Line2D(
        xdata=(xpos,xpos),
        ydata=(l, h),
        color = color,
        linewidth = 0.5,
        antialiased=True
    )
    bar = Rectangle(
        xy=(xpos-barWidth/2.0, lowestBarPosition),
        width=barWidth,
        height=barHeight,
        facecolor=color,
        edgecolor=color
    )
    bar.set_alpha(alpha)
    return line, bar

def plotChart(ax, quotes, barWidth = 0.2, colorUpper = 'g', colorLower = 'r', alpha=1.0):
    xcoords = []
    xpos = 0
    for quote in quotes:
        line, bar = addBar(xpos, quote, barWidth, colorUpper, colorLower, alpha)
        xcoords.append(xpos)
        xpos+=(barWidth+1.0)
        ax.add_line(line)
        ax.add_patch(bar)
        ax.add_patch(bar)
    ax.plot()
    return xcoords

def alignXAxis(fig, ax, xcoords, ycoords, tickFrequency):
    plt.xticks(xcoords[-1:0:-tickFrequency], ycoords[-1:0:-tickFrequency])
    fig.autofmt_xdate()
    plt.grid()

def plot(df, quotes):
    fig, ax = plt.subplots()
    xcoords = plotChart(ax, quotes, 1)
    alignXAxis(fig, ax, xcoords, df['Date'].values, tickFrequency)
    plt.show()


# df=pandas.read_csv('eurusd_d.csv')
# size = 1000
# tickFrequency = size//20

# df=df.tail(size)
# quotes = df[['Date', 'Open', 'High', 'Low', 'Close']].values

# plot(df, quotes)


