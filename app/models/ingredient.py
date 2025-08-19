from app import db
from datetime import datetime

class Ingredient(db.Model):
    """Modelo para ingredientes"""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    unit_of_measure = db.Column(db.String(20), nullable=False)  # kg, g, ml, l, unidade, etc
    price_per_unit = db.Column(db.Numeric(10, 2))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, name, unit_of_measure, description=None, price_per_unit=None):
        self.name = name
        self.unit_of_measure = unit_of_measure
        self.description = description
        self.price_per_unit = price_per_unit
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'unit_of_measure': self.unit_of_measure,
            'price_per_unit': float(self.price_per_unit) if self.price_per_unit else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
