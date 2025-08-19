from app import db
from app.models.category import Category

def seed_categories():
    """Seeds iniciais para categorias"""
    categories_data = [
        {
            'name': 'Entrada',
            'description': 'Pratos servidos como entrada da refeição'
        },
        {
            'name': 'Prato Principal',
            'description': 'Pratos principais das refeições'
        },
        {
            'name': 'Sobremesa',
            'description': 'Doces e sobremesas'
        },
        {
            'name': 'Bebida',
            'description': 'Bebidas diversas, alcoólicas e não alcoólicas'
        },
        {
            'name': 'Lanche',
            'description': 'Lanches e petiscos'
        },
        {
            'name': 'Salada',
            'description': 'Saladas e pratos vegetarianos'
        },
        {
            'name': 'Massa',
            'description': 'Massas, pizza e pratos italianos'
        },
        {
            'name': 'Grelhado',
            'description': 'Carnes e peixes grelhados'
        }
    ]
    
    created_count = 0
    
    for category_data in categories_data:
        # Verifica se a categoria já existe
        existing_category = Category.query.filter_by(name=category_data['name']).first()
        
        if not existing_category:
            category = Category(
                name=category_data['name'],
                description=category_data['description']
            )
            db.session.add(category)
            created_count += 1
    
    try:
        db.session.commit()
        print(f"✅ Seeder de categorias concluído: {created_count} categorias criadas")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no seeder de categorias: {str(e)}")
        return False
