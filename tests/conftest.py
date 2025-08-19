import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Cria um cliente de teste"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Cria um runner para comandos CLI"""
    return app.test_cli_runner()
