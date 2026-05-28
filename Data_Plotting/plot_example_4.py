import yfinance as yf
import mplfinance as mpf



intel_df = yf.download("INTC",period="5y")

print(intel_df.head())

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

intel_df["ma5"] = intel_df["Close"].rolling(window=5).mean()
intel_df["ma25"] = intel_df["Close"].rolling(window=25).mean()
intel_df["ma75"] = intel_df["Close"].rolling(window=75).mean()

addp = [
    mpf.make_addplot(intel_df["ma5"], color="blue"),
    mpf.make_addplot(intel_df["ma25"], color="green"),
    mpf.make_addplot(intel_df["ma75"], color="red")
]

mpf.plot(intel_df, type="candle", figratio = (2,1), addplot = addp, style= "nightclouds", volume = True)
