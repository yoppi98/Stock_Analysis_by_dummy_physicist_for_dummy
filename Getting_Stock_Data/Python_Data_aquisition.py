import yfinance as yf

df = yf.download("AAPL", period="5y")

print("First 5 rows:")
print(df.head())

print("Last 5 rows:")
print(df.tail())

print(df.index)