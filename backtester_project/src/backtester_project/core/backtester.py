import pandas as pd
from .result import Result
from .strategy import Strategy


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%% Classe principale de Backtesting %%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class Backtester:
    def __init__(self, data, transaction_cost=0.001, slippage=0.0005):
        """
        Parameters
        ----------
        data : pd.DataFrame or pd.Series
            Série(s) de prix — une colonne = un actif.
        transaction_cost : float
            Taux de frais de transaction (ex: 0.001 = 0.1%)
        slippage : float
            Taux de slippage par trade (ex: 0.0005 = 0.05%)
        """
        if isinstance(data, pd.Series):
            data = data.to_frame("Asset")
        self.data = data
        self.assets = data.columns
        self.transaction_cost = transaction_cost
        self.slippage = slippage

    def run_backtest(self, strategy, rebalance_freq=1):
        """
        Lance le backtest d'une stratégie sur un ou plusieurs actifs.
        """
        n = len(self.data)
        positions = {asset: 0 for asset in self.assets}
        trades = []
        portfolio_returns = []

        # Boucle principale
        for i in range(1, n):
            prices_today = self.data.iloc[i]
            prices_yesterday = self.data.iloc[i - 1]

            # Rebalance à fréquence donnée
            if i % rebalance_freq == 0 or i == 1:
                new_positions = strategy.get_position(self.data.iloc[:i], positions.copy())

                for asset in self.assets:
                    old_pos = positions[asset]
                    new_pos = new_positions.get(asset, old_pos)

                    # Si la position change, on enregistre un trade et applique coûts
                    if new_pos != old_pos:
                        trade_cost = abs(new_pos - old_pos) * prices_today[asset] * (
                            self.transaction_cost + self.slippage
                        )
                        trades.append((i, asset, prices_today[asset], new_pos, trade_cost))
                        positions[asset] = new_pos

            # Calcul du rendement du portefeuille
            daily_returns = {
                asset: (prices_today[asset] - prices_yesterday[asset]) / prices_yesterday[asset]
                for asset in self.assets
            }

            # PnL 
            portfolio_return = sum(
                positions[asset] * daily_returns[asset] for asset in self.assets
            )

            # Retirer les coûts de trading (distribués sur le jour de trade)
            if trades and trades[-1][0] == i:
                total_cost = sum(t[4] for t in trades if t[0] == i)
                portfolio_return -= total_cost / len(self.assets)

            portfolio_returns.append(portfolio_return)

        total_return = sum(portfolio_returns)
        return Result(total_return, trades, len(self.data), portfolio_returns)

