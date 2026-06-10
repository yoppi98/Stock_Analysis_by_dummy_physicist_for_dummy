import yfinance as yf 
import pandas as pd
import datetime as dt
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import talib as ta
import plotly.graph_objects as go
import plotly.io as pio

ticker = "INTC"
name = "Intel Corp" 

intel_df= yf.download("INTC", period="5y")
intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

plot_df = intel_df["2025-12-01":]
plot_df.index = pd.to_datetime(plot_df.index).strftime("%m-%d-%y")

data = [go.Candlestick(x = plot_df.index, open = plot_df["Open"], 
        high = plot_df["High"], low = plot_df["Low"], close=plot_df["Close"],
        increasing_line_color = "green",
        increasing_line_width = 1.0,
        increasing_fillcolor = "green",
        decreasing_line_color = "red",
        decreasing_line_width = 1.0,
        decreasing_fillcolor = "red")
        ]

layout = {"title" : {"text":"{} {}".format(ticker, name), "x": 0.5},
          "xaxis": {"title": "Date", "rangeslider": {"visible": False} ,"type": "category","tickvals": plot_df.index[::2]},
          "yaxis": {"title": "Stock Price (Dollar)", "side":"left", "tickformat":","},
          "plot_bgcolor": "white","paper_bgcolor": "white"
}

fig = go.Figure(data=data, layout=go.Layout(layout))

fig.update_xaxes(showgrid=True, gridcolor="lightgray")
fig.update_yaxes(showgrid=True, gridcolor="lightgray")

fig.show()