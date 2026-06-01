import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import talib as ta


intel_df = yf.download("INTC",period="5y")

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

Close = intel_df["Close"]

intel_df["ma25"] = ta.SMA(intel_df["Close"], 25)

intel_df["Upper1"], _, intel_df["Lower1"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 1, nbdevdn = 1, matype = ta.MA_Type.SMA)

intel_df["Upper2"], _, intel_df["Lower2"]=ta.BBANDS(Close, timeperiod = 25, nbdevup = 2, nbdevdn = 2, matype = ta.MA_Type.SMA)

addp = [
    mpf.make_addplot(intel_df["ma25"], color="blue",width =0.5),
    mpf.make_addplot(intel_df["Upper1"], color = "red", width = 0.5),
    mpf.make_addplot(intel_df["Lower1"], color = "red", width = 0.5),
    mpf.make_addplot(intel_df["Upper2"], color = "green", width = 0.5),
    mpf.make_addplot(intel_df["Lower2"], color = "green", width = 0.5)
]

fig, axes = mpf.plot(intel_df, type="candle", figratio = (2,1), addplot = addp, style= "nightclouds"
         , volume = True, returnfig = True)

legend_lines = [
    Line2D([0], [0], color="blue", label="MA25"),
    Line2D([0], [0], color="red", label="sigma"),
    Line2D([0], [0], color="green", label="2-sigma")
]

axes[0].legend(handles=legend_lines, loc="upper left")

plt.show()