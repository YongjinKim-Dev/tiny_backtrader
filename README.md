# tiny_backtrader

tiny_backtrader is a lightweight Python library for backtesting trading strategies with OHLCV (Open, High, Low, Close, Volume) time-series data. Despite its minimal code footprint, it supports key functionalities such as slippage, fees, custom strategies, and intra-/daily data handling.

## Features

- Flexible Data Input  
  Accepts either a list of dictionaries (each containing date, open, high, low, close, volume, etc.) or a pandas DataFrame.

- Pluggable Strategy  
  Easily inject custom buy/sell conditions by defining simple Python functions (or lambdas) and passing them to the Strategy class.

- Slippage & Fees  
  Simulate real-world trading conditions by specifying slippage (sl) and transaction fees (fee).

- Intraday or Daily Support  
  Works with any time-based granularity. You can set the start/end parameters to include full date-time strings if necessary.

- Results & Reporting  
  Returns a list of executed trades, final capital, total profit, and the percentage yield.

## Installation

Simply clone this repository and import the modules directly from the project files:

~~~
bash
git clone https://github.com/username/tiny_backtrader.git
cd tiny_backtrader
~~~

## Usage

### 1. Import the Library

~~~
python
from tiny_backtrader.engine import run_backtest, Strategy
~~~

### 2. Prepare Your Data (with MA indicator)

If you already have a moving average (MA) calculated, add it as a column or key in your dataset. For example:

~~~
python
data = [
    {'date': '2022-01-01', 'open': '99', 'high': '101', 'low': '98', 'close': '100', 'volume': '1000', 'ma': '99.5'},
    {'date': '2022-01-02', 'open': '104','high': '106','low': '103','close': '105','volume': '1100','ma': '102'},
    # ...
]
~~~

Or, if using pandas:

~~~
python
import pandas as pd

df = pd.DataFrame(data)
# df['ma'] = df['close'].astype(float).rolling(window=5).mean()
~~~

### 3. Define a Strategy (using MA)

~~~
python
def buy_condition(dataset, i):
    if i == 0:
        return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close < ma_val

def sell_condition(dataset, i):
    if i == 0:
        return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close > ma_val

my_strategy = Strategy(buy=buy_condition, sell=sell_condition)
~~~

### 4. Run the Backtest

~~~
python
trades, final_capital, profit, yield_pct = run_backtest(
    data,
    cap=10000,
    start="2022-01-01",
    end="2022-01-10",
    strat=my_strategy,
    sl=0.01,
    fee=0.001
)

print("Trades:", trades)
print("Final Capital:", final_capital)
print("Profit:", profit)
print("Yield:", yield_pct, "%")
~~~

### 5. Testing

~~~
bash
pytest
~~~

- Unit tests are located under the test directory and cover list-based data, pandas DataFrame, and intraday data scenarios.

## License

This project is distributed under the MIT License. You are free to modify and distribute this code, but please include the original license.

