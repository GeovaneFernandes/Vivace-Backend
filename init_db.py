#!/usr/bin/env python
"""
Script para inicializar o banco de dados do projeto Vivace
"""

import os
import sys
from flask_migrate import init, migrate, upgrade

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def init_db():
    """Inicializa o banco de dados com migrações"""
    app = create_app()
    
    with app.app_context():
        try:
            # Verifica se o diretório migrations já existe
            if not os.path.exists('migrations'):
                print("🔧 Inicializando Flask-Migrate...")
                init()
                print("✅ Flask-Migrate inicializado com sucesso!")
            else:
                print("📁 Diretório migrations já existe, pulando inicialização...")
            
            # Cria a primeira migração
            print("🔄 Criando migração inicial...")
            migrate(message='Initial migration')
            print("✅ Migração criada com sucesso!")
            
            # Aplica as migrações
            print("🚀 Aplicando migrações ao banco de dados...")
            upgrade()
            print("✅ Banco de dados criado/atualizado com sucesso!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar banco de dados: {str(e)}")
            return False

if __name__ == '__main__':
    success = init_db()
    if success:
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("🌱 Execute 'python seeders/run_seeders.py' para popular com dados iniciais")
    else:
        print("\n💥 Falha na inicialização do banco de dados")
        sys.exit(1)
