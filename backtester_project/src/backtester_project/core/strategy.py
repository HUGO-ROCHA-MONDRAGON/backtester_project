from abc import ABC, abstractmethod

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%% Classe abstraite de stratégie %%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Strategy(ABC):
    """
    Classe abstraite de base pour les stratégies de trading.
    Toutes les stratégies concrètes doivent hériter de cette classe
    et implémenter la méthode get_position().
    """

    # La méthode get_position est declaree comme abstraite par @abstractmethod : 
    # toute sous-classe devra obligatoirement la redéfinir.
    # Elle determine la position (achat, vente, neutre) a prendre
    # a partir des données historiques et de la position actuelle.
    @abstractmethod
    def get_position(self, historical_data, current_position):
        pass

    # Methode pour calibrer (fit) la stratégie sur des données.
    # Par défaut, elle ne fait rien (return None), mais peut être surchargée
    # dans les sous-classes si la stratégie nécessite un apprentissage.
    def fit(self, data):
        return None

