from flask import Blueprint, request
from app import db
from app.models.company import Company
from app.utils.auth import token_required
from app.utils.helpers import success_response, error_response, paginate_query, validate_email

bp = Blueprint('companies', __name__, url_prefix='/api/companies')

@bp.route('', methods=['GET'])
def get_companies():
    """Lista todas as empresas com paginação"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = Company.query.filter_by(is_active=True)
        
        if search:
            query = query.filter(Company.name.contains(search))
        
        query = query.order_by(Company.name)
        
        result = paginate_query(query, page, per_page)
        
        if result is None:
            return error_response("Erro na paginação", 500)
        
        return success_response(
            data=result,
            message="Empresas recuperadas com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar empresas: {str(e)}", 500)

@bp.route('/<int:company_id>', methods=['GET'])
def get_company(company_id):
    """Recupera uma empresa específica"""
    try:
        company = Company.query.filter_by(id=company_id, is_active=True).first()
        
        if not company:
            return error_response("Empresa não encontrada", 404)
        
        return success_response(
            data=company.to_dict(),
            message="Empresa recuperada com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao buscar empresa: {str(e)}", 500)

@bp.route('', methods=['POST'])
@token_required
def create_company(current_user):
    """Cria uma nova empresa"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Validações
        if not data.get('name'):
            return error_response("Nome é obrigatório", 400)
        
        if data.get('email') and not validate_email(data['email']):
            return error_response("Email inválido", 400)
        
        # Verifica se a empresa já existe (mesmo nome ou email)
        if Company.query.filter_by(name=data['name'], is_active=True).first():
            return error_response("Empresa com este nome já existe", 400)
        
        if data.get('email') and Company.query.filter_by(email=data['email'], is_active=True).first():
            return error_response("Email já está em uso", 400)
        
        # Cria a empresa
        company = Company(
            name=data['name'],
            description=data.get('description'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        
        # Campos opcionais adicionais
        if 'city' in data:
            company.city = data['city']
        if 'state' in data:
            company.state = data['state']
        if 'zip_code' in data:
            company.zip_code = data['zip_code']
        if 'website' in data:
            company.website = data['website']
        
        db.session.add(company)
        db.session.commit()
        
        return success_response(
            data=company.to_dict(),
            message="Empresa criada com sucesso",
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao criar empresa: {str(e)}", 500)

@bp.route('/<int:company_id>', methods=['PUT'])
@token_required
def update_company(current_user, company_id):
    """Atualiza uma empresa"""
    try:
        company = Company.query.filter_by(id=company_id, is_active=True).first()
        
        if not company:
            return error_response("Empresa não encontrada", 404)
        
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Atualiza os campos
        if 'name' in data:
            # Verifica se o nome não está sendo usado por outra empresa
            existing = Company.query.filter_by(name=data['name'], is_active=True).first()
            if existing and existing.id != company.id:
                return error_response("Nome já está em uso", 400)
            company.name = data['name']
        
        if 'email' in data:
            if data['email'] and not validate_email(data['email']):
                return error_response("Email inválido", 400)
            # Verifica se o email não está sendo usado por outra empresa
            existing = Company.query.filter_by(email=data['email'], is_active=True).first()
            if existing and existing.id != company.id:
                return error_response("Email já está em uso", 400)
            company.email = data['email']
        
        # Atualiza outros campos
        fields_to_update = [
            'description', 'phone', 'address', 'city', 
            'state', 'zip_code', 'website'
        ]
        
        for field in fields_to_update:
            if field in data:
                setattr(company, field, data[field])
        
        db.session.commit()
        
        return success_response(
            data=company.to_dict(),
            message="Empresa atualizada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao atualizar empresa: {str(e)}", 500)

@bp.route('/<int:company_id>', methods=['DELETE'])
@token_required
def delete_company(current_user, company_id):
    """Deleta (desativa) uma empresa"""
    try:
        company = Company.query.filter_by(id=company_id, is_active=True).first()
        
        if not company:
            return error_response("Empresa não encontrada", 404)
        
        # Verifica se há receitas usando esta empresa
        if company.recipes:
            return error_response("Não é possível deletar empresa que possui receitas associadas", 400)
        
        # Soft delete - marca como inativa
        company.is_active = False
        db.session.commit()
        
        return success_response(
            message="Empresa deletada com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao deletar empresa: {str(e)}", 500)
