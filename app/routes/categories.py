from flask import Blueprint, request
from app import db
from app.models.category import Category
from app.utils.auth import token_required
from app.utils.helpers import success_response, error_response, paginate_query

bp = Blueprint('categories', __name__, url_prefix='/api/categories')

@bp.route('', methods=['GET'])
def get_categories():
    """Lista todas as categorias com paginação"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = Category.query.filter_by(is_active=True)
        
        if search:
            query = query.filter(Category.name.contains(search))
        
        query = query.order_by(Category.name)
        
        result = paginate_query(query, page, per_page)
        
        if result is None:
            return error_response("Erro na paginação", 500)
        
        return success_response(
            data=result,
            message="Categorias recuperadas com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar categorias: {str(e)}", 500)

@bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Recupera uma categoria específica"""
    try:
        category = Category.query.filter_by(id=category_id, is_active=True).first()
        
        if not category:
            return error_response("Categoria não encontrada", 404)
        
        return success_response(
            data=category.to_dict(),
            message="Categoria recuperada com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar categoria: {str(e)}", 500)

@bp.route('', methods=['POST'])
@token_required
def create_category(current_user):
    """Cria uma nova categoria"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Validações
        if not data.get('name'):
            return error_response("Nome é obrigatório", 400)
        
        # Verifica se a categoria já existe
        if Category.query.filter_by(name=data['name'], is_active=True).first():
            return error_response("Categoria já existe", 400)
        
        # Cria a categoria
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        
        db.session.add(category)
        db.session.commit()
        
        return success_response(
            data=category.to_dict(),
            message="Categoria criada com sucesso",
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao criar categoria: {str(e)}", 500)

@bp.route('/<int:category_id>', methods=['PUT'])
@token_required
def update_category(current_user, category_id):
    """Atualiza uma categoria"""
    try:
        category = Category.query.filter_by(id=category_id, is_active=True).first()
        
        if not category:
            return error_response("Categoria não encontrada", 404)
        
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Atualiza os campos
        if 'name' in data:
            # Verifica se o nome não está sendo usado por outra categoria
            existing = Category.query.filter_by(name=data['name'], is_active=True).first()
            if existing and existing.id != category.id:
                return error_response("Nome já está em uso", 400)
            category.name = data['name']
        
        if 'description' in data:
            category.description = data['description']
        
        db.session.commit()
        
        return success_response(
            data=category.to_dict(),
            message="Categoria atualizada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao atualizar categoria: {str(e)}", 500)

@bp.route('/<int:category_id>', methods=['DELETE'])
@token_required
def delete_category(current_user, category_id):
    """Deleta (desativa) uma categoria"""
    try:
        category = Category.query.filter_by(id=category_id, is_active=True).first()
        
        if not category:
            return error_response("Categoria não encontrada", 404)
        
        # Verifica se há receitas usando esta categoria
        if category.recipes:
            return error_response("Não é possível deletar categoria que possui receitas associadas", 400)
        
        # Soft delete - marca como inativa
        category.is_active = False
        db.session.commit()
        
        return success_response(
            message="Categoria deletada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao deletar categoria: {str(e)}", 500)
