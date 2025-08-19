from app import db
from datetime import datetime

# Tabela de relacionamento Many-to-Many entre Recipe e Ingredient
recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True),
    db.Column('quantity', db.Numeric(10, 2), nullable=False),
    db.Column('unit', db.String(20), nullable=False)
)

class Recipe(db.Model):
    """Modelo para receitas"""
    __tablename__ = 'recipes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # tempo em minutos
    cook_time = db.Column(db.Integer)  # tempo em minutos
    servings = db.Column(db.Integer, default=1)
    difficulty_level = db.Column(db.String(20), default='medium')  # easy, medium, hard
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients, lazy='subquery',
                                backref=db.backref('recipes', lazy=True))
    creator = db.relationship('User', backref='recipes', lazy=True)
    
    def __init__(self, name, instructions, category_id=None, company_id=None, created_by=None):
        self.name = name
        self.instructions = instructions
        self.category_id = category_id
        self.company_id = company_id
        self.created_by = created_by
    
    def add_ingredient(self, ingredient, quantity, unit):
        """Adiciona um ingrediente à receita"""
        # Implementação para adicionar ingrediente com quantidade específica
        pass
    
    def to_dict(self, include_ingredients=False):
        """Converte o objeto para dicionário"""
        recipe_dict = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'difficulty_level': self.difficulty_level,
            'category_id': self.category_id,
            'company_id': self.company_id,
            'created_by': self.created_by,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_ingredients:
            recipe_dict['ingredients'] = [ingredient.to_dict() for ingredient in self.ingredients]
        
        return recipe_dict
    
    def __repr__(self):
        return f'<Recipe {self.name}>'
