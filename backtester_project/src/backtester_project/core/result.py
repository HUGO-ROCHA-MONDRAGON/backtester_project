import math
import matplotlib.pyplot as plt
import pandas as pd

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%% Classe des Resultats %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class Result:
    def __init__(self, total_return, trades, n_days, returns=None):
        self.total_return = total_return
        self.trades = trades
        self.n_days = n_days
        self.returns = returns if returns is not None else []

        # Moyenne et variance sécurisées
        self.mean_r = sum(self.returns) / len(self.returns) if self.returns else 0

    def __repr__(self):
        return f"Result(total_return={self.total_return:.4f}, trades={self.trades})"

    # === Performance brute ===
    def total_perf(self):
        ann_perf = (1 + self.total_return) ** (252 / self.n_days) - 1
        return f"Total Return: {self.total_return*100:.2f}%, Annualized Return: {ann_perf*100:.2f}%"

    # === Variance et volatilité ===
    def sigma_squared(self):
        if not self.returns or len(self.returns) < 2:
            return 0
        variance = sum((r - self.mean_r) ** 2 for r in self.returns) / (len(self.returns) - 1)
        return variance

    def volatility(self):
        return math.sqrt(self.sigma_squared())

    # === Sharpe Ratio ===
    def sharpe_ratio(self, risk_free_rate=0.0):
        if not self.returns or len(self.returns) < 2:
            return 0
        std_r = self.volatility()
        if std_r == 0:
            return 0
        daily_sharpe = (self.mean_r - risk_free_rate / 252) / std_r
        return daily_sharpe * math.sqrt(252)

    # === Sortino Ratio ===
    def sortino_ratio(self, risk_free_rate=0.0):
        if not self.returns or len(self.returns) < 2:
            return 0
        downside_returns = [r for r in self.returns if r < 0]
        if not downside_returns:
            return float("inf")  # aucun jour négatif = ratio infini
        downside_std = math.sqrt(
            sum((r - risk_free_rate / 252) ** 2 for r in downside_returns) / len(downside_returns)
        )
        mean_excess = self.mean_r - risk_free_rate / 252
        daily_sortino = mean_excess / downside_std
        return daily_sortino * math.sqrt(252)

    # === Max Drawdown ===
    def max_drawdown(self):
        if not self.returns:
            return 0
        equity_curve = [1]
        for r in self.returns:
            equity_curve.append(equity_curve[-1] * (1 + r))
        peak = equity_curve[0]
        max_dd = 0
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_dd = max(max_dd, drawdown)
        return max_dd

    # === Nombre de trades ===
    def num_trades(self):
        return len(self.trades)

    # === Pourcentage de trades gagnants ===
    def win_rate(self):
        if not self.trades or len(self.trades) < 2:
            return 0

        # On suppose que les trades sont (index, prix, position)
        wins = 0
        total = 0
        for i in range(1, len(self.trades)):
            entry_price = self.trades[i-1][1]
            exit_price = self.trades[i][1]
            direction = self.trades[i-1][2]

            pnl = (exit_price - entry_price) * direction
            total += 1
            if pnl > 0:
                wins += 1

        return wins / total if total > 0 else 0

    def plot(self, backend="matplotlib"):
        if not self.returns:
            print("Aucune donnée de rendement à tracer.")
            return

        equity_curve = [1]
        for r in self.returns:
            equity_curve.append(equity_curve[-1] * (1 + r))

        if backend == "matplotlib":
            plt.figure(figsize=(8,4))
            plt.plot(equity_curve, label="Équity Curve")
            plt.title("Performance de la stratégie")
            plt.xlabel("Période")
            plt.ylabel("Valeur cumulée")
            plt.legend()
            plt.show()

        elif backend == "seaborn":
            import seaborn as sns
            sns.set(style="whitegrid")
            plt.figure(figsize=(8,4))
            sns.lineplot(x=range(len(equity_curve)), y=equity_curve)
            plt.title("Performance (Seaborn)")
            plt.show()

        elif backend == "plotly":
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=equity_curve, mode="lines", name="Équity Curve"))
            fig.update_layout(title="Performance (Plotly)",
                              xaxis_title="Période", yaxis_title="Valeur cumulée")
            fig.show()

        else:
            raise ValueError("Backend non supporté. Choisissez: matplotlib / seaborn / plotly.")
    
    @staticmethod
    def compare(*results):
        """
        Compare les performances de plusieurs stratégies.
        Affiche un résumé sous forme de tableau texte.
        """
        if not results:
            print("Aucun résultat fourni.")
            return

        headers = [
            "Stratégie", "Total Return (%)", "Ann. Return (%)",
            "Sharpe", "Sortino", "Max DD (%)", "Trades", "Win Rate (%)"
        ]

        print("\n=== COMPARAISON DES STRATÉGIES ===")
        print("{:<15} {:>15} {:>15} {:>10} {:>10} {:>12} {:>10} {:>12}".format(*headers))
        print("-" * 95)

        for i, r in enumerate(results, 1):
            ann_perf = (1 + r.total_return) ** (252 / r.n_days) - 1
            row = [
                f"Strat {i}",
                f"{r.total_return*100:.2f}",
                f"{ann_perf*100:.2f}",
                f"{r.sharpe_ratio():.2f}",
                f"{r.sortino_ratio():.2f}",
                f"{r.max_drawdown()*100:.2f}",
                f"{r.num_trades()}",
                f"{r.win_rate()*100:.2f}"
            ]
            print("{:<15} {:>15} {:>15} {:>10} {:>10} {:>12} {:>10} {:>12}".format(*row))


