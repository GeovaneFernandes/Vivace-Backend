# Seeders para popular o banco de dados com dados iniciais
from .user_seeder import seed_users
from .category_seeder import seed_categories
from .ingredient_seeder import seed_ingredients
from .company_seeder import seed_companies

__all__ = [
    'seed_users',
    'seed_categories',
    'seed_ingredients',
    'seed_companies'
]
