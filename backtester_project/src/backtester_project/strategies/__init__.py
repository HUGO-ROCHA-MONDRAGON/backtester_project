# On importe ici les differentes strategies disponibles dans le package "strategies".
# Cela permet de les rendre accessibles directement a l'import du package,
# sans avoir a specifier le nom du sous-module (ex : strategies.momentum).

from .buy_and_hold import BuyAndHold
from .momentum import MomentumStrategy
from .mean_reversion import MeanReversionStrategy

# La variable speciale __all__ definit la liste des objets (classes, fonctions, etc.)
# qui seront importes lorsque l’on fait :
#     from strategies import *
#
# Cela permet :
# A) de controler explicitement ce qui est expose a l'exterieur du module,
# B) de clarifier la structure publique de ton package,
# C) et d'eviter d'importer accidentellement des fonctions internes ou temporaires.
#
# Ici, on rend visibles uniquement les trois classes principales de strategies.
__all__ = ["BuyAndHold", "MomentumStrategy", "MeanReversionStrategy"]
