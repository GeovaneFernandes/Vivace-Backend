import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from seeders.user_seeder import seed_users
from seeders.category_seeder import seed_categories
from seeders.ingredient_seeder import seed_ingredients
from seeders.company_seeder import seed_companies

def run_all_seeders():
    """Executa todos os seeders na ordem correta"""
    print("🌱 Iniciando processo de seeding...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Cria as tabelas se não existirem
            db.create_all()
            print("📋 Tabelas do banco de dados verificadas/criadas")
            
            # Executa os seeders na ordem correta
            seeders = [
                ("Usuários", seed_users),
                ("Categorias", seed_categories),
                ("Ingredientes", seed_ingredients),
                ("Empresas", seed_companies)
            ]
            
            success_count = 0
            
            for name, seeder_func in seeders:
                print(f"\n🔄 Executando seeder: {name}")
                if seeder_func():
                    success_count += 1
                else:
                    print(f"❌ Falha no seeder: {name}")
            
            print(f"\n✅ Processo de seeding concluído!")
            print(f"📊 Sucesso: {success_count}/{len(seeders)} seeders executados com sucesso")
            
            if success_count == len(seeders):
                print("\n🎉 Todos os dados iniciais foram inseridos no banco de dados!")
                print("🔑 Usuários criados:")
                print("   - admin@vivace.com (senha: admin123)")
                print("   - chef@vivace.com (senha: chef123)")
                print("   - user@vivace.com (senha: user123)")
            
        except Exception as e:
            print(f"❌ Erro durante o processo de seeding: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    run_all_seeders()
