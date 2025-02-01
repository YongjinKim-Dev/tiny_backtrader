# tiny_backtrader

tiny_backtrader is a lightweight Python library for backtesting trading strategies with OHLCV (Open, High, Low, Close, Volume) time-series data. Despite its minimal code footprint, it supports key functionalities such as slippage, fees, custom strategies, and intra-/daily data handling.

## Features

- Flexible Data Input  
  Accepts either a list of dictionaries (each containing date, open, high, low, close, volume, etc.) or a pandas DataFrame.

- Pluggable Strategy  
  Easily inject custom buy/sell conditions by defining simple Python functions (or lambdas) and passing them to the `Strategy` class.

- Slippage & Fees  
  Simulate real-world trading conditions by specifying slippage (`sl`) and transaction fees (`fee`).

- Intraday or Daily Support  
  Works with any time-based granularity. You can set the start/end parameters to include full date-time strings if necessary.

- Results & Reporting  
  Returns a list of executed trades, final capital, total profit, and the percentage yield.

## Installation

Simply clone this repository and place the `tiny_backtrader` directory where your Python code can import it:

~~~bash
git clone https://github.com/username/tiny_backtrader.git
cd tiny_backtrader
~~~

If you prefer to keep `tiny_backtrader` at the same directory level as your own script (e.g., `example.py`), Python will automatically find it when using relative imports. Otherwise, make sure to add its path to your `PYTHONPATH`.

## Usage

### Directory Example

Your project might look like this:

~~~
tiny_backtrader/
├── tiny_backtrader/
│   ├── engine.py
│   └── ...
└── example.py
~~~

### 1. Run with an Example

The following example assumes you have Python 3 installed.  
Copy and paste this entire code snippet into a file (e.g., `example.py`) at the same directory level as `tiny_backtrader` (see above structure), then run:

~~~bash
python example.py
~~~

~~~python
import pandas as pd

# If you're running locally and the tiny_backtrader folder is in the same directory:
from tiny_backtrader.engine import run_backtest, Strategy

data = [
    {'date': '2022-01-01', 'open': '99', 'high': '101', 'low': '98', 'close': '100', 'volume': '1000', 'ma': '99.5'},
    {'date': '2022-01-02', 'open': '104','high': '106','low': '103','close': '105','volume': '1100','ma': '102'},
    {'date': '2022-01-03', 'open': '101','high': '103','low': '100','close': '102','volume': '1200','ma': '103'},
    {'date': '2022-01-04', 'open': '105','high': '106','low': '104','close': '105','volume': '1300','ma': '104.5'}
]

df = pd.DataFrame(data)

def buy_condition(dataset, i):
    if i == 0: return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close < ma_val

def sell_condition(dataset, i):
    if i == 0: return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close > ma_val

my_strategy = Strategy(buy=buy_condition, sell=sell_condition)

trades, final_capital, profit, yield_pct = run_backtest(
    df,
    cap=10000,
    start="2022-01-01",
    end="2022-01-04",
    strat=my_strategy,
    sl=0.01,
    fee=0.001
)

print("Trades:", trades)
print("Final Capital:", final_capital)
print("Profit:", profit)
print("Yield:", yield_pct, "%")
~~~

### 2. Further Testing

If you want to run the built-in tests, simply install pytest and run:

~~~bash
pytest
~~~

- Unit tests are located under the `test` directory and cover list-based data, pandas DataFrame, and intraday data scenarios.

## License

This project is distributed under the MIT License. You are free to modify and distribute this code, but please include the original license.
