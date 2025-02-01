class Strategy:
    def __init__(self, buy=None, sell=None, price_key='close'):
        self.buy = buy; self.sell = sell; self.price_key = price_key
    def __call__(self, data, i):
        if i==0: return None
        p = float(data[i][self.price_key])
        if self.buy and self.buy(data,i): return ('b',p)
        if self.sell and self.sell(data,i): return ('s',p)
        return None

def run_backtest(data, cap, start, end, strat, sl=0, fee=0):
    init = cap
    d = sorted([r for r in (data.to_dict('records') if hasattr(data,'to_dict') else data)
                if start <= str(r['date']) <= end], key=lambda r: str(r['date']))
    pos, trades = 0, []
    for i, r in enumerate(d):
        res = strat(d, i)
        if not res: continue
        sig, p = res if isinstance(res, tuple) else (res, float(r[strat.price_key]))
        if sig=='b' and not pos:
            pos = cap*(1-fee)/(p*(1+sl)); cap = 0; trades.append((r['date'],'buy',p))
        elif sig=='s' and pos:
            cap = pos*p*(1-sl)*(1-fee); pos = 0; trades.append((r['date'],'sell',p))
    final_cap = cap + pos*float(d[-1]['close'])*(1-sl)*(1-fee)
    return trades, final_cap, final_cap-init, (final_cap/init-1)*100

