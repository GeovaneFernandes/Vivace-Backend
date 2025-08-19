from app import db
from app.models.ingredient import Ingredient

def seed_ingredients():
    """Seeds iniciais para ingredientes"""
    ingredients_data = [
        # Carnes
        {'name': 'Frango (Peito)', 'unit_of_measure': 'kg', 'description': 'Peito de frango sem osso', 'price_per_unit': 15.99},
        {'name': 'Carne Bovina (Alcatra)', 'unit_of_measure': 'kg', 'description': 'Alcatra bovina', 'price_per_unit': 35.99},
        {'name': 'Peixe (Salmão)', 'unit_of_measure': 'kg', 'description': 'Filé de salmão', 'price_per_unit': 45.99},
        
        # Vegetais
        {'name': 'Tomate', 'unit_of_measure': 'kg', 'description': 'Tomate maduro', 'price_per_unit': 6.99},
        {'name': 'Cebola', 'unit_of_measure': 'kg', 'description': 'Cebola branca', 'price_per_unit': 4.99},
        {'name': 'Alho', 'unit_of_measure': 'kg', 'description': 'Alho descascado', 'price_per_unit': 12.99},
        {'name': 'Cenoura', 'unit_of_measure': 'kg', 'description': 'Cenoura baby', 'price_per_unit': 5.99},
        {'name': 'Batata', 'unit_of_measure': 'kg', 'description': 'Batata inglesa', 'price_per_unit': 3.99},
        {'name': 'Pimentão', 'unit_of_measure': 'kg', 'description': 'Pimentão colorido', 'price_per_unit': 8.99},
        
        # Temperos e Ervas
        {'name': 'Sal', 'unit_of_measure': 'kg', 'description': 'Sal refinado', 'price_per_unit': 2.99},
        {'name': 'Pimenta do Reino', 'unit_of_measure': 'g', 'description': 'Pimenta do reino moída', 'price_per_unit': 0.05},
        {'name': 'Orégano', 'unit_of_measure': 'g', 'description': 'Orégano seco', 'price_per_unit': 0.08},
        {'name': 'Manjericão', 'unit_of_measure': 'g', 'description': 'Manjericão fresco', 'price_per_unit': 0.15},
        
        # Laticínios
        {'name': 'Leite', 'unit_of_measure': 'l', 'description': 'Leite integral', 'price_per_unit': 4.99},
        {'name': 'Queijo Mussarela', 'unit_of_measure': 'kg', 'description': 'Queijo mussarela fatiado', 'price_per_unit': 28.99},
        {'name': 'Queijo Parmesão', 'unit_of_measure': 'kg', 'description': 'Queijo parmesão ralado', 'price_per_unit': 45.99},
        {'name': 'Manteiga', 'unit_of_measure': 'kg', 'description': 'Manteiga sem sal', 'price_per_unit': 18.99},
        
        # Óleos e Vinagres
        {'name': 'Azeite de Oliva', 'unit_of_measure': 'l', 'description': 'Azeite extra virgem', 'price_per_unit': 25.99},
        {'name': 'Óleo de Soja', 'unit_of_measure': 'l', 'description': 'Óleo de soja refinado', 'price_per_unit': 6.99},
        {'name': 'Vinagre Balsâmico', 'unit_of_measure': 'ml', 'description': 'Vinagre balsâmico', 'price_per_unit': 0.08},
        
        # Massas e Grãos
        {'name': 'Macarrão Espaguete', 'unit_of_measure': 'kg', 'description': 'Macarrão espaguete', 'price_per_unit': 4.99},
        {'name': 'Arroz', 'unit_of_measure': 'kg', 'description': 'Arroz branco longo', 'price_per_unit': 5.99},
        {'name': 'Feijão Preto', 'unit_of_measure': 'kg', 'description': 'Feijão preto', 'price_per_unit': 7.99},
        
        # Outros
        {'name': 'Ovos', 'unit_of_measure': 'unidade', 'description': 'Ovos de galinha', 'price_per_unit': 0.75},
        {'name': 'Farinha de Trigo', 'unit_of_measure': 'kg', 'description': 'Farinha de trigo especial', 'price_per_unit': 3.99},
        {'name': 'Açúcar', 'unit_of_measure': 'kg', 'description': 'Açúcar cristal', 'price_per_unit': 4.99}
    ]
    
    created_count = 0
    
    for ingredient_data in ingredients_data:
        # Verifica se o ingrediente já existe
        existing_ingredient = Ingredient.query.filter_by(name=ingredient_data['name']).first()
        
        if not existing_ingredient:
            ingredient = Ingredient(
                name=ingredient_data['name'],
                unit_of_measure=ingredient_data['unit_of_measure'],
                description=ingredient_data.get('description'),
                price_per_unit=ingredient_data.get('price_per_unit')
            )
            db.session.add(ingredient)
            created_count += 1
    
    try:
        db.session.commit()
        print(f"✅ Seeder de ingredientes concluído: {created_count} ingredientes criados")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no seeder de ingredientes: {str(e)}")
        return False
