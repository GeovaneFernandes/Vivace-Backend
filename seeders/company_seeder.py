from app import db
from app.models.company import Company

def seed_companies():
    """Seeds iniciais para empresas"""
    companies_data = [
        {
            'name': 'Restaurante Vivace',
            'description': 'Restaurante especializado em culinária italiana contemporânea',
            'email': 'contato@restaurantevivace.com',
            'phone': '(11) 3456-7890',
            'address': 'Rua das Flores, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234-567',
            'website': 'https://www.restaurantevivace.com'
        },
        {
            'name': 'Pizzaria Bella Vita',
            'description': 'Pizzaria artesanal com massa fermentada naturalmente',
            'email': 'contato@bellavita.com',
            'phone': '(11) 2345-6789',
            'address': 'Avenida Paulista, 456',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01310-100',
            'website': 'https://www.bellavita.com'
        },
        {
            'name': 'Café Gourmet',
            'description': 'Cafeteria especializada em cafés especiais e doces artesanais',
            'email': 'contato@cafegourmet.com',
            'phone': '(11) 4567-8901',
            'address': 'Rua Augusta, 789',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01305-000',
            'website': 'https://www.cafegourmet.com'
        },
        {
            'name': 'Bistrô do Chef',
            'description': 'Bistrô contemporâneo com menu sazonal',
            'email': 'contato@bistrodochef.com',
            'phone': '(11) 5678-9012',
            'address': 'Rua Oscar Freire, 321',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01426-001',
            'website': 'https://www.bistrodochef.com'
        }
    ]
    
    created_count = 0
    
    for company_data in companies_data:
        # Verifica se a empresa já existe
        existing_company = Company.query.filter_by(email=company_data['email']).first()
        
        if not existing_company:
            company = Company(
                name=company_data['name'],
                description=company_data['description'],
                email=company_data['email'],
                phone=company_data['phone'],
                address=company_data['address']
            )
            
            # Adiciona campos opcionais
            company.city = company_data['city']
            company.state = company_data['state']
            company.zip_code = company_data['zip_code']
            company.website = company_data['website']
            
            db.session.add(company)
            created_count += 1
    
    try:
        db.session.commit()
        print(f"✅ Seeder de empresas concluído: {created_count} empresas criadas")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro no seeder de empresas: {str(e)}")
        return False
