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

Close= intel_df["Close"]

intel_df["ma5"]= ta.SMA(Close, 5)
intel_df["ma25"]= ta.SMA(Close, 25)

cross = intel_df["ma5"] > intel_df["ma25"]
cross_shift = cross.shift(1)

intel_df["cross"] = intel_df["ma5"] > intel_df["ma25"]
intel_df["cross_shift"] = cross_shift

temp_gc = (cross != cross_shift) & (cross==True)
temp_dc = (cross != cross_shift) & (cross==False)

intel_df["temp_gc"] = temp_gc
intel_df["temp_dc"] = temp_dc

intel_df["gc_point"] = intel_df["ma5"].where(intel_df["temp_gc"])
intel_df["dc_point"] = intel_df["ma25"].where(intel_df["temp_dc"])

intel_df["Upper1"], _, intel_df["Lower1"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 1, nbdevdn = 1, matype = ta.MA_Type.SMA)
intel_df["Upper2"], _, intel_df["Lower2"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 2, nbdevdn = 2, matype = ta.MA_Type.SMA)

plot_df = intel_df["2025-12-01":]
plot_df.index = pd.to_datetime(plot_df.index).strftime("%m-%d-%y")

data = [go.Candlestick(x = plot_df.index, open = plot_df["Open"], 
        high = plot_df["High"], low = plot_df["Low"], close=plot_df["Close"],
        increasing_line_color = "green",
        increasing_line_width = 1.0,
        increasing_fillcolor = "green",
        decreasing_line_color = "red",
        decreasing_line_width = 1.0,
        decreasing_fillcolor = "red"),

        go.Scatter(x=plot_df.index, y = plot_df["ma5"], name = "MA5", line=dict(color="#ff00ff", width=1.5)),

        go.Scatter(x=plot_df.index, y = plot_df["ma25"], name = "MA25", line={"color":"blue", "width":1.5}),

        go.Scatter(x=plot_df.index, y= plot_df["gc_point"], name="Golden Cross",  mode="markers", 
                   marker=dict(size=20, color="yellow", symbol="triangle-up",
                           line=dict(color="black", width=2))),

        go.Scatter(x=plot_df.index, y= plot_df["dc_point"], name="Dead Cross", mode="markers", 
                   marker=dict(color="red",size=20,symbol="triangle-down",line=dict(color="black", width=2))),
        
        go.Scatter(x=plot_df.index, y = plot_df["Upper2"], name="",line={"color": "white", "width":0}),

        go.Scatter(x=plot_df.index, y = plot_df["Lower2"], name="Bollinger Band",line={"color": "white", "width":0},
                   fill="tonexty", fillcolor="rgba(0, 102, 255, 0.12)"),
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