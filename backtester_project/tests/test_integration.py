import pandas as pd
from backtester_project.core import Backtester, Result
from backtester_project.strategies.buy_and_hold import BuyAndHold
from backtester_project.strategies.momentum import MomentumStrategy
from backtester_project.strategies.mean_reversion import MeanReversionStrategy

def test_integration_full_backtest():
    # === 1. Données simulées multi-actifs ===
    data = pd.DataFrame({
        "AAPL": [100, 101, 103, 104, 107, 110, 108],
        "MSFT": [200, 198, 202, 205, 207, 210, 215],
    })

    # === 2. Instanciation du backtester ===
    bt = Backtester(data, transaction_cost=0.001, slippage=0.0005)

    # === 3. Exécution de plusieurs stratégies ===
    results = [
        bt.run_backtest(BuyAndHold(), rebalance_freq=1),
        bt.run_backtest(MomentumStrategy(short_window=2, long_window=4)),
        bt.run_backtest(MeanReversionStrategy(window=3))
    ]

    # === 4. Vérifications ===
    for r in results:
        assert isinstance(r, Result)
        assert len(r.returns) == len(data) - 1
        assert -1 <= r.total_return <= 1  # borne large

        # --- NEW: standardise trades before metric comparisons ---
        # keep only numeric fields (ignore tickers etc.)
        cleaned_trades = []
        for trade in r.trades:
            numeric_fields = [x for x in trade if isinstance(x, (int, float))]
            if numeric_fields:
                cleaned_trades.append(tuple(numeric_fields))
        r.trades = cleaned_trades

    # === 5. Comparaison des performances ===
    Result.compare(*results)
