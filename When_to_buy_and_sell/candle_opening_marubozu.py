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
name = "Intel corp" 

intel_df= yf.download(ticker, period="5y")
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

intel_df["RSI14"]=ta.RSI(Close, timeperiod=14)
intel_df["RSI28"]=ta.RSI(Close, timeperiod=28)

intel_df["slowK"], intel_df["slowD"]= ta.STOCH(intel_df["High"], intel_df["Low"],
                Close, fastk_period=5, slowk_period=3, slowd_matype=0,
                slowd_period=3, slowk_matype=0)

intel_df["macd"],intel_df["macd_signal"],intel_df["hist"]=ta.MACD(Close, 
                        fastperiod=12, slowperiod= 26, signalperiod=9)

intel_df["Marubozu"] = ta.CDLBELTHOLD(intel_df["Open"],intel_df["High"],intel_df["Low"],intel_df["Close"])
intel_df["Marubozu_Text"] = intel_df["Marubozu"].replace({100: "Buy",-100: "Sell",0: ""})

intel_df["Marubozu_Marker"] = intel_df["High"].where(intel_df["Marubozu"] != 0)

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

        go.Scatter(yaxis="y1",x=plot_df.index, y = plot_df["ma5"], name = "MA5", line=dict(color="#ff00ff", width=1.5)),

        go.Scatter(yaxis="y1",x=plot_df.index, y = plot_df["ma25"], name = "MA25", line={"color":"blue", "width":1.5}),

        go.Scatter(yaxis="y1",x=plot_df.index, y= plot_df["gc_point"], name="Golden Cross",  mode="markers", 
                   marker=dict(size=10, color="yellow", symbol="triangle-up",
                           line=dict(color="black", width=2))),

        go.Scatter(yaxis="y1",x=plot_df.index, y= plot_df["dc_point"], name="Dead Cross", mode="markers", 
                   marker=dict(color="red",size=10,symbol="triangle-down",line=dict(color="black", width=2))),
        
        go.Scatter(yaxis="y1",x=plot_df.index, y = plot_df["Upper2"], name="",line={"color": "white", "width":0}),

        go.Scatter(yaxis="y1",x=plot_df.index, y = plot_df["Lower2"], name="Bollinger Band",line={"color": "white", "width":0},
                   fill="tonexty", fillcolor="rgba(0, 102, 255, 0.12)"),

        go.Scatter(yaxis="y1", x=plot_df.index, y=plot_df["Marubozu_Marker"], mode="markers+text",name= "MaruBozu", text=plot_df["Marubozu_Text"],
                        textposition="top center", marker=dict(size=14,color=plot_df["Marubozu"].map({100: "blue",-100: "black",0: "rgba(0,0,0,0)"}),
                        symbol=plot_df["Marubozu"].map({100: "star",-100: "x",0: "circle"}),
                        line=dict(color="black",width=1))),

        go.Scatter(yaxis="y3", x=plot_df.index, y= plot_df["macd"], name="macd", line={"color":"pink", "width":1}),
        go.Scatter(yaxis="y3", x=plot_df.index, y= plot_df["macd_signal"], name="macd_signal", line={"color":"cyan", "width":1}),
        go.Bar(yaxis="y3", x=plot_df.index, y= plot_df["hist"], name="histgram", marker=dict(color="gray"),
                        opacity=0.4),

        go.Scatter(yaxis= "y4", x=plot_df.index, y = plot_df["RSI14"], name= "RSI14", line={"color": "black", "width" :0.5}),
        go.Scatter(yaxis= "y4", x=plot_df.index, y = plot_df["RSI28"], name= "RSI28", line={"color": "red", "width" :0.5}),

        go.Scatter(yaxis="y5", x=plot_df.index, y = plot_df["slowK"], name="SlowK", line={"color": "red", "width":0.5}),
        go.Scatter(yaxis="y5", x=plot_df.index, y = plot_df["slowD"], name="SlowD", line={"color": "blue", "width":0.5}),

        go.Bar(x=plot_df.index, y=plot_df["Volume"], name="Volume", yaxis="y6",marker=dict(color="lightgray"),
        opacity=0.7)
        ]

layout = {"height":1000, "title":{"text":"{} {}".format(ticker, name), "x": 0.5},
          "xaxis": {"rangeslider": {"visible": False} ,"type": "category","tickvals": plot_df.index[::30],
                    "anchor": "y2"},
          "yaxis": { "domain":[0.59, 1.00] ,"title": "Stock Price (Dollar)", "side":"left", "tickformat":","},
          "yaxis2": {"domain":[0.5, 0.59]},
          "yaxis3": {"domain":[0.4, 0.495], "title": "MACD"},
          "yaxis4": {"domain":[0.2, 0.395],"title": "RSI"},
          "yaxis5": {"domain":[0.1, 0.195],"title":"Stochastics"},
          "yaxis6": {"domain": [0, 0.095], "title": "Volume", "showgrid":True},
          "plot_bgcolor": "white","paper_bgcolor": "white",
          "margin": {"l": 70,"r": 30,"t": 70,"b": 90
    }
}

fig = go.Figure(data=data, layout=go.Layout(layout))

fig.update_xaxes(showgrid=True, gridcolor="lightgray")
fig.update_yaxes(showgrid=True, gridcolor="lightgray")

fig.add_hline(y=70, line_dash="dash", line_color="orange", line_width=1, yref="y4")
fig.add_hline(y=30, line_dash="dash", line_color="cyan", line_width=1, yref="y4")

fig.add_hline(y=80, line_dash="dash", line_color="orange", line_width=1, yref="y5")
fig.add_hline(y=20, line_dash="dash", line_color="cyan", line_width=1, yref="y5")

fig.show()