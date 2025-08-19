# Importa todos os modelos para que sejam registrados no SQLAlchemy
from .user import User
from .category import Category
from .ingredient import Ingredient
from .company import Company
from .recipe import Recipe, recipe_ingredients

__all__ = [
    'User',
    'Category', 
    'Ingredient',
    'Company',
    'Recipe',
    'recipe_ingredients'
]
