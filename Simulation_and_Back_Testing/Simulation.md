# Simulating Buy and Sell in the Stock Market

So far, I learned how to analyze the stock market and how to use strategies to decide when to buy and sell stocks.

The next step is to simulate buying and selling using the rules we define.

For example, we can make rules such as:

```text
Buy when a golden cross appears
Sell when a dead cross appears
```

Then, we can apply these rules to past stock price data.

This process is called **backtesting**.

## What Is Backtesting?

**Backtesting** means testing a trading strategy using past stock market data.

In simple words:

```text
Past stock data
→ apply buy/sell rules
→ simulate trades
→ check profit or loss
```

Backtesting is useful because it allows us to check whether our strategy would have worked in the past.

For example, we can test questions such as:

```text
Is MA5 and MA25 a good combination?
Is MA20 better than MA25?
When should we sell after buying?
Which strategy gives better profit?
```

## Why Backtesting Is Important

After backtesting, it is important to check the result and improve the strategy.

This feedback process helps us understand what worked and what did not work.

For example, if one moving average setting does not give good results, we can try another setting.

```text
Test strategy
→ check result
→ change parameters
→ test again
```

This allows us to find better parameters, such as the best number of days for the moving average.

## Backtesting with Python

We can do backtesting using Python.

One useful Python library for this is:

```python
backtesting.py
```

This library allows us to define a trading strategy and simulate buying and selling using historical stock data.

In the next section, I will use `backtesting.py` to simulate a simple trading strategy.

## backtesting.py

To implement a trading rule, we need to define when to buy and when to sell.

In `backtesting.py`, these rules are written inside a **Strategy class**.

There are mainly four steps.

## Step 1: Define the Strategy Class Name

First, we define the name of the strategy class.

It is better to use a simple name that is easy to remember.

For example:

```python
class SmaCross(Strategy):
```

Here, `SmaCross` means that this strategy uses a moving average cross.

## Step 2: Define Parameters

Second, we define parameters as members of the class.

For example:

```python
n1 = 5
n2 = 25
```

Here, `n1` and `n2` are the moving average periods.

The good thing is that these parameters can be changed during backtesting.

Because of this, we can later search for better values.

For example, we can test whether MA5 and MA25 are good, or whether MA10 and MA50 are better.

## Step 3: Define the `init()` Method

Third, we define the `init()` method.

The `init()` method is used to prepare indicators before the backtest starts.

For example, we can calculate moving averages, RSI, MACD, or other technical indicators here.

```python
def init(self):
    pass
```

In simple words:

```text
init() = prepare indicators
```

## Step 4: Define the `next()` Method

Finally, we define the `next()` method.

The `next()` method is called step by step as the backtest moves through the stock data.

Inside this method, we write the actual trading rules.

For example:

```python
def next(self):
    if buy_condition:
        self.buy()

    if sell_condition:
        self.position.close()
```

Here:

| Code | Meaning |
|---|---|
| `self.buy()` | Buy the stock |
| `self.position.close()` | Close the current position |

In simple words:

```text
next() = decide buy or sell at each time step
```

## Summary

The basic structure of a `backtesting.py` strategy is:

```python
class MyStrategy(Strategy):

    # 1. Define parameters
    n1 = 5
    n2 = 25

    # 2. Prepare indicators
    def init(self):
        pass

    # 3. Define buy/sell rules
    def next(self):
        pass
```

Therefore, the `Strategy` class is the place where we write our trading logic.

The `init()` method prepares the indicators, and the `next()` method decides when to buy and sell.

Let's try to use the **SMA method** in `backtesting.py`.

```python
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class MyStrategy(Strategy):
    n1 = 5
    n2 = 25

    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()

        elif crossover(self.sma2, self.sma1):
            self.position.close()
```

Here, `n1` and `n2` are the moving average periods.

```python
n1 = 5
n2 = 25
```

In the `init()` method, we calculate two simple moving averages.

```python
self.sma1 = self.I(SMA, self.data.Close, self.n1)
self.sma2 = self.I(SMA, self.data.Close, self.n2)
```

Here, `self.I()` tells `backtesting.py` that this is an indicator.

In the `next()` method, we define the buy and sell rules.

```python
if crossover(self.sma1, self.sma2):
    self.buy()
```

This means:

```text
If the short moving average crosses above the long moving average,
buy the stock.
```

And:

```python
elif crossover(self.sma2, self.sma1):
    self.position.close()
```

This means:

```text
If the long moving average crosses above the short moving average,
close the position.
```

In simple words:

| Condition | Meaning | Action |
|---|---|---|
| MA5 crosses above MA25 | Golden cross | Buy |
| MA25 crosses above MA5 | Dead cross | Sell / close position |