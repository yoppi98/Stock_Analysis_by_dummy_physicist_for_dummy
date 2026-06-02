import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import talib as ta


intel_df = yf.download("INTC",period="5y")

print(intel_df.head())

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

Close = intel_df["Close"]

intel_df["ma5"] = ta.SMA(intel_df["Close"], 5)
intel_df["ma25"] = ta.SMA(intel_df["Close"], 25)

intel_df["Upper1"], _, intel_df["Lower1"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 1, nbdevdn = 1, matype = ta.MA_Type.SMA)

intel_df["Upper2"], _, intel_df["Lower2"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 2, nbdevdn = 2, matype = ta.MA_Type.SMA)


intel_df["ma5_dr"] = (intel_df["Close"]-intel_df["ma5"])/intel_df["ma5"]*100
intel_df["ma25_dr"] = (intel_df["Close"]-intel_df["ma25"])/intel_df["ma25"]*100


addp = [
    mpf.make_addplot(intel_df["ma5"], color="blue"),
    mpf.make_addplot(intel_df["ma25"], color="green"),

    mpf.make_addplot(intel_df["Upper1"], color = "red", width = 0.5),
    mpf.make_addplot(intel_df["Lower1"], color = "red", width = 0.5),
    mpf.make_addplot(intel_df["Upper2"], color = "purple", width = 0.5),
    mpf.make_addplot(intel_df["Lower2"], color = "purple", width = 0.5),

    mpf.make_addplot(intel_df["ma5_dr"], color = "yellow", panel=2, ylabel="MA5 DR (%)"),
    mpf.make_addplot(intel_df["ma25_dr"], color = "orange", panel=3, ylabel="MA25 DR (%)")
    ]

fig, axes = mpf.plot(intel_df, type="candle", figratio = (2,1), addplot = addp, style= "nightclouds"
         , volume = True, returnfig = True)

legend_lines = [
    Line2D([0], [0], color="blue", label="MA5"),
    Line2D([0], [0], color="green", label="MA25"),
    Line2D([0], [0], color="red", label="sigma"),
    Line2D([0], [0], color="green", label="2-sigma")
]

axes[0].legend(handles=legend_lines, loc="upper left")

plt.show()

