import pytest
from backtester_poo.core.strategy import Strategy

# Une stratégie minimale pour les tests
class DummyStrategy(Strategy):
    def get_position(self, historical_data, current_position):
        return {col: 1 for col in historical_data.columns}

def test_strategy_is_abstract():
    with pytest.raises(TypeError):
        Strategy()  # On ne peut pas instancier la classe abstraite

def test_dummy_strategy_get_position():
    import pandas as pd
    data = pd.DataFrame({"AAPL": [100, 101, 102]})
    strat = DummyStrategy()
    pos = strat.get_position(data, {})
    assert isinstance(pos, dict)
    assert "AAPL" in pos
    assert pos["AAPL"] == 1
