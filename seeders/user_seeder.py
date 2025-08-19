from app import db
from app.models.user import User

def seed_users():
    """Seeds iniciais para usuários"""
    users_data = [
        {
            'name': 'Administrador',
            'email': 'admin@vivace.com',
            'password': 'admin123'
        },
        {
            'name': 'Chef Demo',
            'email': 'chef@vivace.com',
            'password': 'chef123'
        },
        {
            'name': 'Usuário Demo',
            'email': 'user@vivace.com',
            'password': 'user123'
        }
    ]
    
    created_count = 0
    
    for user_data in users_data:
        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(email=user_data['email']).first()
        
        if not existing_user:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password']
            )
            db.session.add(user)
            created_count += 1
    
    try:
        db.session.commit()
        print(f"✅ Seeder de usuários concluído: {created_count} usuários criados")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no seeder de usuários: {str(e)}")
        return False
