import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import talib as ta


intel_df = yf.download("INTC",period="5y")

print(intel_df.head())

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

intel_df["ma5"] = ta.SMA(intel_df["Close"], 5)

intel_df["ma25"] = ta.SMA(intel_df["Close"], 25)

intel_df["ma75"] = ta.SMA(intel_df["Close"], 75)

addp = [
    mpf.make_addplot(intel_df["ma5"], color="blue"),
    mpf.make_addplot(intel_df["ma25"], color="green"),
    mpf.make_addplot(intel_df["ma75"], color="red")
]

fig, axes = mpf.plot(intel_df, type="candle", figratio = (2,1), addplot = addp, style= "nightclouds"
         , volume = True, returnfig = True)

legend_lines = [
    Line2D([0], [0], color="blue", label="MA5"),
    Line2D([0], [0], color="green", label="MA25"),
    Line2D([0], [0], color="red", label="MA75")
]

axes[0].legend(handles=legend_lines, loc="upper left")

plt.show()