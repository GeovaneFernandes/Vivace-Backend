from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
from app import db
from app.models.recipe import Recipe
from app.models.category import Category
from app.models.company import Company
from app.models.ingredient import Ingredient
from app.utils.auth import token_required
from app.utils.helpers import success_response, error_response, paginate_query

bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

@bp.route('', methods=['GET'])
def get_recipes():
    """Lista todas as receitas com paginação"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        company_id = request.args.get('company_id', type=int)
        
        query = Recipe.query.filter_by(is_active=True)
        
        if search:
            query = query.filter(Recipe.name.contains(search))
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if company_id:
            query = query.filter_by(company_id=company_id)
        
        query = query.order_by(Recipe.name)
        
        result = paginate_query(query, page, per_page)
        
        if result is None:
            return error_response("Erro na paginação", 500)
        
        return success_response(
            data=result,
            message="Receitas recuperadas com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar receitas: {str(e)}", 500)

@bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Recupera uma receita específica com ingredientes"""
    try:
        recipe = Recipe.query.filter_by(id=recipe_id, is_active=True).first()
        
        if not recipe:
            return error_response("Receita não encontrada", 404)
        
        return success_response(
            data=recipe.to_dict(include_ingredients=True),
            message="Receita recuperada com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar receita: {str(e)}", 500)

@bp.route('', methods=['POST'])
@token_required
def create_recipe(current_user):
    """Cria uma nova receita"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Validações obrigatórias
        required_fields = ['name', 'instructions']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Campo '{field}' é obrigatório", 400)
        
        # Validações opcionais com verificação de existência
        if data.get('category_id'):
            category = Category.query.filter_by(id=data['category_id'], is_active=True).first()
            if not category:
                return error_response("Categoria não encontrada", 404)
        
        if data.get('company_id'):
            company = Company.query.filter_by(id=data['company_id'], is_active=True).first()
            if not company:
                return error_response("Empresa não encontrada", 404)
        
        # Cria a receita
        recipe = Recipe(
            name=data['name'],
            instructions=data['instructions'],
            category_id=data.get('category_id'),
            company_id=data.get('company_id'),
            created_by=current_user.id
        )
        
        # Campos opcionais
        optional_fields = [
            'description', 'prep_time', 'cook_time', 
            'servings', 'difficulty_level'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(recipe, field, data[field])
        
        db.session.add(recipe)
        db.session.flush()  # Para obter o ID antes do commit
        
        # Adiciona ingredientes se fornecidos
        if 'ingredients' in data and isinstance(data['ingredients'], list):
            for ing_data in data['ingredients']:
                if not all(k in ing_data for k in ['ingredient_id', 'quantity', 'unit']):
                    return error_response("Ingredientes devem ter ingredient_id, quantity e unit", 400)
                
                ingredient = Ingredient.query.filter_by(
                    id=ing_data['ingredient_id'], 
                    is_active=True
                ).first()
                
                if not ingredient:
                    return error_response(f"Ingrediente {ing_data['ingredient_id']} não encontrado", 404)
                
                recipe.ingredients.append(ingredient)
        
        db.session.commit()
        
        return success_response(
            data=recipe.to_dict(include_ingredients=True),
            message="Receita criada com sucesso",
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao criar receita: {str(e)}", 500)

@bp.route('/<int:recipe_id>', methods=['PUT'])
@token_required
def update_recipe(current_user, recipe_id):
    """Atualiza uma receita"""
    try:
        recipe = Recipe.query.filter_by(id=recipe_id, is_active=True).first()
        
        if not recipe:
            return error_response("Receita não encontrada", 404)
        
        # Verifica se o usuário é o criador da receita (ou pode implementar roles)
        if recipe.created_by != current_user.id:
            return error_response("Você não tem permissão para editar esta receita", 403)
        
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Atualiza campos básicos
        basic_fields = [
            'name', 'description', 'instructions', 'prep_time', 
            'cook_time', 'servings', 'difficulty_level'
        ]
        
        for field in basic_fields:
            if field in data:
                setattr(recipe, field, data[field])
        
        # Atualiza category_id se fornecido
        if 'category_id' in data:
            if data['category_id']:
                category = Category.query.filter_by(id=data['category_id'], is_active=True).first()
                if not category:
                    return error_response("Categoria não encontrada", 404)
            recipe.category_id = data['category_id']
        
        # Atualiza company_id se fornecido
        if 'company_id' in data:
            if data['company_id']:
                company = Company.query.filter_by(id=data['company_id'], is_active=True).first()
                if not company:
                    return error_response("Empresa não encontrada", 404)
            recipe.company_id = data['company_id']
        
        # Atualiza ingredientes se fornecidos
        if 'ingredients' in data:
            recipe.ingredients.clear()  # Remove ingredientes atuais
            
            if isinstance(data['ingredients'], list):
                for ing_data in data['ingredients']:
                    if not all(k in ing_data for k in ['ingredient_id', 'quantity', 'unit']):
                        return error_response("Ingredientes devem ter ingredient_id, quantity e unit", 400)
                    
                    ingredient = Ingredient.query.filter_by(
                        id=ing_data['ingredient_id'], 
                        is_active=True
                    ).first()
                    
                    if not ingredient:
                        return error_response(f"Ingrediente {ing_data['ingredient_id']} não encontrado", 404)
                    
                    recipe.ingredients.append(ingredient)
        
        db.session.commit()
        
        return success_response(
            data=recipe.to_dict(include_ingredients=True),
            message="Receita atualizada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao atualizar receita: {str(e)}", 500)

@bp.route('/<int:recipe_id>', methods=['DELETE'])
@token_required
def delete_recipe(current_user, recipe_id):
    """Deleta (desativa) uma receita"""
    try:
        recipe = Recipe.query.filter_by(id=recipe_id, is_active=True).first()
        
        if not recipe:
            return error_response("Receita não encontrada", 404)
        
        # Verifica se o usuário é o criador da receita (ou pode implementar roles)
        if recipe.created_by != current_user.id:
            return error_response("Você não tem permissão para deletar esta receita", 403)
        
        # Soft delete - marca como inativa
        recipe.is_active = False
        db.session.commit()
        
        return success_response(
            message="Receita deletada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao deletar receita: {str(e)}", 500)
