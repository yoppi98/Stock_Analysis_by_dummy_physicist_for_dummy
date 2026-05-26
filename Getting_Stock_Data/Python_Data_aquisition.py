import yfinance as yf
import matplotlib.pyplot as plt

df = yf.download("AAPL", period="5y")

print("First 5 rows:")
print(df.head())

print("Last 5 rows:")
print(df.tail())

print(df[df.index >= "2024-01-01"].head())

print(df["Close"].head())

df["Close"].plot()

plt.show()