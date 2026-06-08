import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import talib as ta

intel_df = yf.download("INTC" , period= "5y")
intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

Close = intel_df["Close"]

intel_df["ma5"] = ta.SMA(intel_df["Close"], 5)
intel_df["ma25"] = ta.SMA(intel_df["Close"], 25)

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


plot_df = intel_df["2025-12-01":]

addp = [
    mpf.make_addplot(plot_df["ma5"], color="yellow", width=1),
    mpf.make_addplot(plot_df["ma25"], color="blue", width=1),
    mpf.make_addplot(plot_df["Upper1"], color="red", width=0.5),
    mpf.make_addplot(plot_df["Lower1"], color="red", width=0.5),
    mpf.make_addplot(plot_df["Upper2"], color="green", width=0.5),
    mpf.make_addplot(plot_df["Lower2"], color="green", width=0.5),
    mpf.make_addplot(plot_df["gc_point"], type = "scatter", 
                     markersize = 150, marker = "^", color="red"),
    mpf.make_addplot(plot_df["dc_point"], type = "scatter", 
                     markersize = 150, marker = "v", color="gray"),
    mpf.make_addplot(plot_df["RSI14"], color = "white", width=0.5, panel =2),
    mpf.make_addplot(plot_df["RSI28"], color = "red", width=0.5, panel =2)
]

fig, axes = mpf.plot(plot_df, type="candle", figratio = (2,1), addplot = addp, style= "nightclouds"
         , volume = True, returnfig = True)

legend_lines = [
    Line2D([0], [0], color="yellow", label="MA5"),
    Line2D([0], [0], color="blue", label="MA25"),
    Line2D([0], [0], color="red", label="1-sigma Bollinger Band"),
    Line2D([0], [0], color="green", label="2-sigma Bollinger Band"),
    Line2D([0], [0], marker="^", color="red", linestyle="None", label="Golden Cross"),
    Line2D([0], [0], marker="v", color="gray", linestyle="None", label="Dead Cross")
]

axes[0].legend(handles=legend_lines, loc="upper left")

axes[4].axhline(70, color="orange", linestyle="--", linewidth=1)
axes[4].axhline(30, color="cyan", linestyle="--", linewidth=1)
axes[4].set_ylim(0, 100)

RSI_legend_lines = [
    Line2D([0], [0], color="white", label="RSI 14"),
    Line2D([0], [0], color="red", label="RSI 28"),
    Line2D([0], [0], color="orange", linestyle="--", label="Overbought 70"),
    Line2D([0], [0], color="cyan", linestyle="--", label="Oversold 30")
]

axes[4].legend(handles=RSI_legend_lines, loc="upper left")



plt.show()
