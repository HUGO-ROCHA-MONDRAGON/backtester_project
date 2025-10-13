from abc import ABC, abstractmethod

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%% Classe abstraite de stratégie %%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Strategy(ABC):
    """
    Classe abstraite de base pour les stratégies.
    Doit implémenter get_position().
    """
    @abstractmethod
    def get_position(self, historical_data, current_position):
        pass

    def fit(self, data):
        return None
