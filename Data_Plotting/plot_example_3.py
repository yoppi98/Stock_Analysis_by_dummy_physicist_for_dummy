import yfinance as yf
import mplfinance as mpf



intel_df = yf.download("INTC", period="5y")

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

resampled = intel_df.resample("W")

wdf = resampled.aggregate({
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum"
})

mpf.plot(wdf, type="candle", figratio=(2, 1), volume=True, style = "nightclouds")