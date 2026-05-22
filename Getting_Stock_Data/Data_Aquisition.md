# Stock Price Data Structure

First, I would like to explain some basic stock market terminology.  
This is the minimum knowledge we need to understand stock price data.

You can think of stock market data as a table that records important information about a company and its stock price for a certain day.

## Basic Stock Price Terminology

| Term | Meaning |
|---|---|
| Brand Name | The name of the company or stock. For example, Apple, Toyota, Tesla, etc. |
| Brand Code | The stock code or ticker symbol used to identify the company in the stock market. For example, AAPL for Apple or 7203 for Toyota. |
| Opening Price | The first price of the stock when the market opens. |
| Maximum Price | The highest price of the stock during the trading day. This is also called the high price. |
| Minimum Price | The lowest price of the stock during the trading day. This is also called the low price. |
| Final Price | The last price of the stock when the market closes. This is also called the closing price. |
| Volume | The number of shares traded during the trading day. |

## Example

For example, one row of stock price data may look like this:

| Brand Name | Brand Code | Opening Price | Maximum Price | Minimum Price | Final Price | Volume |
|---|---:|---:|---:|---:|---:|---:|
| Apple | AAPL | 180 | 185 | 178 | 183 | 50,000,000 |

This means that Apple stock started at 180 dollars, reached a highest price of 185 dollars, went down to a lowest price of 178 dollars, and finally closed at 183 dollars.  
The volume means that 50,000,000 shares were traded on that day.

## Why This Data Is Useful

Using this kind of stock price data, we can analyze how the stock price changed during the day.  
For example, we can check whether the price increased or decreased from the opening price to the final price.

## OHLC and OHLCV

This type of stock price data is commonly called **OHLC** or **OHLCV**.

**OHLC** means:

| Letter | Meaning |
|---|---|
| O | Open price |
| H | High price |
| L | Low price |
| C | Close price |

**OHLCV** means OHLC plus volume:

| Letter | Meaning |
|---|---|
| O | Open price |
| H | High price |
| L | Low price |
| C | Close price |
| V | Volume |

So, if the data only contains stock prices, we can call it **OHLC data**.  
If the data also contains trading volume, we can call it **OHLCV data**.

In many stock analysis projects, the basic data table has the following columns:

| Column | Meaning |
|---|---|
| Brand Name | Company or stock name |
| Brand Code | Stock code or ticker symbol |
| Open | First price when the market opens |
| High | Highest price during the trading day |
| Low | Lowest price during the trading day |
| Close | Final price when the market closes |
| Volume | Number of shares traded during the trading day |

## What is the Stock Price Chart ?

