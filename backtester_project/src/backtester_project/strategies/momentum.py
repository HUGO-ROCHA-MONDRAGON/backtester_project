from backtester_project.core.strategy import Strategy

class MomentumStrategy(Strategy):
    """
    Stratégie Momentum :
    Achète l’actif si sa moyenne mobile courte dépasse la longue.
    """
    def __init__(self, short_window=3, long_window=5):
        self.short_window = short_window
        self.long_window = long_window

    def get_position(self, historical_data, current_position):
        positions = {}
        for col in historical_data.columns:
            if len(historical_data) < self.long_window:
                positions[col] = 0
            else:
                short_ma = historical_data[col].iloc[-self.short_window:].mean()
                long_ma = historical_data[col].iloc[-self.long_window:].mean()
                positions[col] = 1 if short_ma > long_ma else -1
        return positions
