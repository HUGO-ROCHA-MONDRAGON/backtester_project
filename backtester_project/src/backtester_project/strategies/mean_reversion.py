from backtester_poo.core.strategy import Strategy

class MeanReversionStrategy(Strategy):
    """
    Stratégie de retour à la moyenne :
    Vend si le prix est au-dessus de la moyenne mobile, achète sinon.
    """
    def __init__(self, window=5):
        self.window = window

    def get_position(self, historical_data, current_position):
        positions = {}
        for col in historical_data.columns:
            if len(historical_data) < self.window:
                positions[col] = 0
            else:
                ma = historical_data[col].iloc[-self.window:].mean()
                last = historical_data[col].iloc[-1]
                positions[col] = -1 if last > ma else 1
        return positions
