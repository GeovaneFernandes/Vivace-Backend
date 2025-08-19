from flask import Blueprint, request
from app import db
from app.models.ingredient import Ingredient
from app.utils.auth import token_required
from app.utils.helpers import success_response, error_response, paginate_query

bp = Blueprint('ingredients', __name__, url_prefix='/api/ingredients')

@bp.route('', methods=['GET'])
def get_ingredients():
    """Lista todos os ingredientes com paginação"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = Ingredient.query.filter_by(is_active=True)
        
        if search:
            query = query.filter(Ingredient.name.contains(search))
        
        query = query.order_by(Ingredient.name)
        
        result = paginate_query(query, page, per_page)
        
        if result is None:
            return error_response("Erro na paginação", 500)
        
        return success_response(
            data=result,
            message="Ingredientes recuperados com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar ingredientes: {str(e)}", 500)

@bp.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Recupera um ingrediente específico"""
    try:
        ingredient = Ingredient.query.filter_by(id=ingredient_id, is_active=True).first()
        
        if not ingredient:
            return error_response("Ingrediente não encontrado", 404)
        
        return success_response(
            data=ingredient.to_dict(),
            message="Ingrediente recuperado com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar ingrediente: {str(e)}", 500)

@bp.route('', methods=['POST'])
@token_required
def create_ingredient(current_user):
    """Cria um novo ingrediente"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Validações
        required_fields = ['name', 'unit_of_measure']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Campo '{field}' é obrigatório", 400)
        
        # Verifica se o ingrediente já existe
        if Ingredient.query.filter_by(name=data['name'], is_active=True).first():
            return error_response("Ingrediente já existe", 400)
        
        # Cria o ingrediente
        ingredient = Ingredient(
            name=data['name'],
            unit_of_measure=data['unit_of_measure'],
            description=data.get('description'),
            price_per_unit=data.get('price_per_unit')
        )
        
        db.session.add(ingredient)
        db.session.commit()
        
        return success_response(
            data=ingredient.to_dict(),
            message="Ingrediente criado com sucesso",
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao criar ingrediente: {str(e)}", 500)

@bp.route('/<int:ingredient_id>', methods=['PUT'])
@token_required
def update_ingredient(current_user, ingredient_id):
    """Atualiza um ingrediente"""
    try:
        ingredient = Ingredient.query.filter_by(id=ingredient_id, is_active=True).first()
        
        if not ingredient:
            return error_response("Ingrediente não encontrado", 404)
        
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Atualiza os campos
        if 'name' in data:
            # Verifica se o nome não está sendo usado por outro ingrediente
            existing = Ingredient.query.filter_by(name=data['name'], is_active=True).first()
            if existing and existing.id != ingredient.id:
                return error_response("Nome já está em uso", 400)
            ingredient.name = data['name']
        
        if 'unit_of_measure' in data:
            ingredient.unit_of_measure = data['unit_of_measure']
        
        if 'description' in data:
            ingredient.description = data['description']
        
        if 'price_per_unit' in data:
            ingredient.price_per_unit = data['price_per_unit']
        
        db.session.commit()
        
        return success_response(
            data=ingredient.to_dict(),
            message="Ingrediente atualizado com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao atualizar ingrediente: {str(e)}", 500)

@bp.route('/<int:ingredient_id>', methods=['DELETE'])
@token_required
def delete_ingredient(current_user, ingredient_id):
    """Deleta (desativa) um ingrediente"""
    try:
        ingredient = Ingredient.query.filter_by(id=ingredient_id, is_active=True).first()
        
        if not ingredient:
            return error_response("Ingrediente não encontrado", 404)
        
        # Soft delete - marca como inativo
        ingredient.is_active = False
        db.session.commit()
        
        return success_response(
            message="Ingrediente deletado com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao deletar ingrediente: {str(e)}", 500)
