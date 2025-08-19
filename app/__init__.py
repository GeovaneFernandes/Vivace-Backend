import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vivace.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Importa os modelos (necessário para migrations)
    from app.models import user, ingredient, recipe, company, category
    
    # Registra as blueprints das rotas
    from app.routes import auth, ingredients, recipes, companies, categories
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(ingredients.bp)
    app.register_blueprint(recipes.bp)
    app.register_blueprint(companies.bp)
    app.register_blueprint(categories.bp)
    
    # Rota de health check
    @app.route('/')
    def health_check():
        return {'message': 'Vivace Backend API is running!', 'status': 'healthy'}, 200
    
    return app
