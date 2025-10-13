from backtester_poo.core.strategy import Strategy

class BuyAndHold(Strategy):
    """
    Stratégie Buy & Hold : reste toujours investi à 100% sur chaque actif.
    """
    def get_position(self, historical_data, current_position):
        return {col: 1 for col in historical_data.columns}
