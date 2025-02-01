import pytest, pandas as pd
from tiny_backtrader.engine import run_backtest, Strategy

@pytest.fixture
def sample_data():
    return [
        {'date':'2022-01-01','open':'99','high':'101','low':'98','close':'100','volume':'1000'},
        {'date':'2022-01-02','open':'104','high':'106','low':'103','close':'105','volume':'1100'},
        {'date':'2022-01-03','open':'101','high':'103','low':'100','close':'102','volume':'1200'},
        {'date':'2022-01-04','open':'107','high':'109','low':'106','close':'108','volume':'1300'}
    ]

@pytest.fixture
def sample_df(sample_data):
    return pd.DataFrame(sample_data)

@pytest.fixture
def sample_intraday():
    return [
        {'date':'2022-01-01 09:30:00','open':'100','high':'101','low':'99','close':'100','volume':'500'},
        {'date':'2022-01-01 09:31:00','open':'100','high':'102','low':'100','close':'101','volume':'600'},
        {'date':'2022-01-01 09:32:00','open':'101','high':'103','low':'101','close':'102','volume':'550'},
        {'date':'2022-01-01 09:33:00','open':'102','high':'104','low':'102','close':'103','volume':'580'}
    ]

def test_run_backtest_list(sample_data):
    def buy(d,i): return float(d[i]['close'])<float(d[i-1]['close'])
    def sell(d,i): return float(d[i]['close'])>float(d[i-1]['close'])
    strat = Strategy(buy=buy, sell=sell)
    trades, final_cap, profit, yr = run_backtest(sample_data, 10000, "2022-01-01", "2022-01-04", strat)
    assert isinstance(trades, list)
    assert isinstance(final_cap, (int, float))
    assert final_cap == 10000 + profit

def test_run_backtest_df(sample_df):
    def buy(d,i): return float(d[i]['close'])<float(d[i-1]['close'])
    def sell(d,i): return float(d[i]['close'])>float(d[i-1]['close'])
    strat = Strategy(buy=buy, sell=sell)
    trades, final_cap, profit, yr = run_backtest(sample_df, 10000, "2022-01-01", "2022-01-04", strat)
    assert isinstance(trades, list)
    assert isinstance(final_cap, (int, float))
    assert final_cap == 10000 + profit

def test_run_backtest_intraday(sample_intraday):
    def buy(d,i): return float(d[i]['close'])<float(d[i-1]['close'])
    def sell(d,i): return float(d[i]['close'])>float(d[i-1]['close'])
    strat = Strategy(buy=buy, sell=sell)
    trades, final_cap, profit, yr = run_backtest(sample_intraday, 10000, "2022-01-01 09:30:00", "2022-01-01 09:33:00", strat)
    assert isinstance(trades, list)
    assert isinstance(final_cap, (int, float))
    assert final_cap == 10000 + profit

