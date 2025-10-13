import pandas as pd
from backtester_poo.core import Backtester, Strategy, Result

class BuyAndHold(Strategy):
    def get_position(self, historical_data, current_position):
        return {col: 1 for col in historical_data.columns}

def test_backtester_runs_single_asset():
    data = pd.Series([100, 102, 104, 108])
    bt = Backtester(data)
    result = bt.run_backtest(BuyAndHold())
    assert isinstance(result, Result)
    assert result.total_return != 0
    assert len(result.returns) == len(data) - 1

def test_backtester_runs_multi_asset():
    data = pd.DataFrame({
        "AAPL": [100, 102, 104],
        "MSFT": [200, 202, 201],
    })
    bt = Backtester(data, transaction_cost=0.001, slippage=0.0005)
    result = bt.run_backtest(BuyAndHold())
    assert isinstance(result, Result)
    assert abs(result.total_return) > 0
