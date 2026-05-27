import yfinance as yf
import mplfinance as mpf



intel_df = yf.download("INTC",period="5y")

print(intel_df.head())

intel_df.columns = intel_df.columns.get_level_values(0)
intel_df = intel_df[["Open", "High", "Low", "Close", "Volume"]]

print("Cleaned data:")
print(intel_df.head())

current_data = intel_df.tail(100)

mpf.plot(intel_df, type="candle", figratio=(2, 1), volume=True, style = "yahoo")