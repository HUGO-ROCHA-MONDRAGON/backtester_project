from backtester_poo.core.result import Result
import math

def test_result_basic_metrics():
    returns = [0.01, -0.005, 0.002, 0.004]
    r = Result(sum(returns), [(0, 100, 1)], len(returns)+1, returns)
    
    assert isinstance(r.total_perf(), str)
    assert math.isclose(r.volatility(), (r.sigma_squared()) ** 0.5)
    assert r.max_drawdown() >= 0
    assert 0 <= r.win_rate() <= 1

def test_sharpe_and_sortino_ratios():
    returns = [0.01, -0.005, 0.002, 0.004]
    r = Result(sum(returns), [(0, 100, 1)], len(returns)+1, returns)
    
    sharpe = r.sharpe_ratio()
    sortino = r.sortino_ratio()
    assert sharpe != 0
    assert sortino != 0
    assert sortino >= sharpe / 2  # Sortino ne devrait pas être aberrant
