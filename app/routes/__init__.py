# Importa todas as blueprints das rotas
from . import auth
from . import ingredients
from . import recipes
from . import companies
from . import categories

__all__ = [
    'auth',
    'ingredients',
    'recipes',
    'companies',
    'categories'
]
