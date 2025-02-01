# tiny_backtrader

tiny_backtrader is a lightweight Python library for backtesting trading strategies with OHLCV (Open, High, Low, Close, Volume) time-series data. Despite its minimal code footprint, it supports key functionalities such as slippage, fees, custom strategies, and intra-/daily data handling.

## Features

- **Flexible Data Input**  
  Accepts either a list of dictionaries (each containing date, open, high, low, close, volume, etc.) or a pandas DataFrame.
- **Pluggable Strategy**  
  Easily inject custom buy/sell conditions by defining simple Python functions (or lambdas) and passing them to the `Strategy` class.
- **Slippage & Fees**  
  Simulate real-world trading conditions by specifying slippage (`sl`) and transaction fees (`fee`).
- **Intraday or Daily Support**  
  Works with any time-based granularity. You can set the start/end parameters to include full date-time strings if necessary.
- **Results & Reporting**  
  Returns a list of executed trades, final capital, total profit, and the percentage yield.

## Installation

Simply clone this repository and place the `tiny_backtrader` directory where your Python code can import it:

~~~bash
git clone https://github.com/username/tiny_backtrader.git
cd tiny_backtrader
~~~

If you plan to run examples without installing the library, ensure that your example file (e.g., `example.py`) is located at the same level as the `tiny_backtrader` package. Otherwise, add its path to your `PYTHONPATH`.

## Directory Structure

A recommended directory structure is as follows:

~~~bash
tiny_backtrader/
├── tiny_backtrader/
│   ├── engine.py
│   └── ...
└── example.py
~~~

This structure indicates that the repository is named `tiny_backtrader` and contains an inner package also named `tiny_backtrader`. The example file is located at the same level as the package, allowing for easy imports.

## Usage

### What You Need to Implement

1. **Data Preparation**  
   - You must provide OHLCV data in either a list of dictionaries or a pandas DataFrame.  
   - Each entry or row should minimally contain:
     - `date` (string or comparable format)
     - `open`, `high`, `low`, `close`, `volume` (numeric values in string or float)

2. **Strategy Definition**  
   - Create two functions or lambdas for buy/sell signals (e.g., based on price comparisons, moving averages, or custom indicators).
   - Pass these functions to the `Strategy` class as `buy` and `sell` arguments.

3. **Backtest Execution**  
   - Call `run_backtest` with:
     - `data` (list or DataFrame)
     - `cap` (initial capital)
     - `start` and `end` (date range)
     - `strat` (your Strategy object)
     - `sl` (slippage ratio)
     - `fee` (transaction fee ratio)

4. **Result Interpretation**  
   - `run_backtest` returns:
     - `trades`: A list of tuples `(date, 'buy'/'sell', price)`.
     - `final_capital`: The total capital after all trades.
     - `profit`: `final_capital - initial_capital`.
     - `yield_pct`: Percentage gain/loss (`(final_capital/initial_capital - 1)*100`).

### 1. Run with an Example

The following example assumes you have Python 3 installed. Copy and paste this entire code snippet into a file (e.g., `example.py`) at the same directory level as the `tiny_backtrader` folder, then run:

~~~bash
python example.py
~~~

~~~python
import pandas as pd
from tiny_backtrader.engine import run_backtest, Strategy

# Sample data with a pre-computed MA (moving average) column
data = [
    {'date': '2022-01-01', 'open': '99', 'high': '101', 'low': '98', 'close': '100', 'volume': '1000', 'ma': '99.5'},
    {'date': '2022-01-02', 'open': '104','high': '106','low': '103','close': '105','volume': '1100','ma': '102'},
    {'date': '2022-01-03', 'open': '101','high': '103','low': '100','close': '102','volume': '1200','ma': '103'},
    {'date': '2022-01-04', 'open': '105','high': '106','low': '104','close': '105','volume': '1300','ma': '104.5'}
]

df = pd.DataFrame(data)

def buy_condition(dataset, i):
    if i == 0:
        return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close < ma_val  # Buy if close < moving average

def sell_condition(dataset, i):
    if i == 0:
        return False
    close = float(dataset[i]['close'])
    ma_val = float(dataset[i]['ma'])
    return close > ma_val  # Sell if close > moving average

my_strategy = Strategy(buy=buy_condition, sell=sell_condition)

# Execute the backtest
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

### 2. How to Execute & Interpret the Output

- **Execution**:  
  - Run `python example.py`. If the `tiny_backtrader` folder is in the correct place, the script will execute without errors.
- **Console Output**:  
  1. **Trades**: Each entry shows the date, whether it was a `'buy'` or `'sell'`, and at what price it occurred.
  2. **Final Capital**: The total capital after the last data point in your specified date range.
  3. **Profit**: Simple difference between final capital and initial capital.
  4. **Yield**: Percentage gain (or loss if negative).

### 3. Further Testing & Customization

- **Testing**:  
  Install pytest and run:
  ~~~bash
  pytest
  ~~~
  Tests are located under the `test` directory, checking list-based data, pandas DataFrame, and intraday data scenarios.
- **Strategy Customization**:  
  You can define any logic in `buy_condition` and `sell_condition` — for instance, combining multiple indicators or thresholds.
- **Advanced Topics**:  
  - Partial fills, multiple positions, or short selling are not included in this minimal example, but can be added by modifying the engine logic.
  - For heavier computations (e.g., calculating technical indicators), integrate with pandas or other libraries to compute new columns (like RSI, Bollinger Bands, etc.).

## License

This project is distributed under the MIT License. You are free to modify and distribute this code, but please include the original license.

