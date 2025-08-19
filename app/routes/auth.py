from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.utils.helpers import success_response, error_response, validate_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Validações
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return error_response(f"Campo '{field}' é obrigatório", 400)
        
        if not validate_email(data['email']):
            return error_response("Email inválido", 400)
        
        if len(data['password']) < 6:
            return error_response("Senha deve ter pelo menos 6 caracteres", 400)
        
        # Verifica se o email já existe
        if User.query.filter_by(email=data['email']).first():
            return error_response("Email já cadastrado", 400)
        
        # Cria o usuário
        user = User(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        db.session.add(user)
        db.session.commit()
        
        return success_response(
            data=user.to_dict(),
            message="Usuário criado com sucesso",
            status_code=201
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao criar usuário: {str(e)}", 500)

@bp.route('/login', methods=['POST'])
def login():
    """Autentica um usuário e retorna o token JWT"""
    try:
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return error_response("Email e senha são obrigatórios", 400)
        
        # Busca o usuário
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return error_response("Email ou senha inválidos", 401)
        
        if not user.is_active:
            return error_response("Usuário inativo", 401)
        
        # Cria o token JWT
        access_token = create_access_token(identity=user.id)
        
        return success_response(
            data={
                'access_token': access_token,
                'user': user.to_dict()
            },
            message="Login realizado com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro no login: {str(e)}", 500)

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Retorna o perfil do usuário autenticado"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return error_response("Usuário não encontrado", 404)
        
        return success_response(
            data=user.to_dict(),
            message="Perfil recuperado com sucesso"
        )
    
    except Exception as e:
        return error_response(f"Erro ao recuperar perfil: {str(e)}", 500)

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Atualiza o perfil do usuário autenticado"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return error_response("Usuário não encontrado", 404)
        
        data = request.get_json()
        
        if not data:
            return error_response("Dados não fornecidos", 400)
        
        # Atualiza os campos permitidos
        if 'name' in data:
            user.name = data['name']
        
        if 'email' in data:
            if not validate_email(data['email']):
                return error_response("Email inválido", 400)
            
            # Verifica se o email não está sendo usado por outro usuário
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user.id:
                return error_response("Email já está em uso", 400)
            
            user.email = data['email']
        
        if 'password' in data:
            if len(data['password']) < 6:
                return error_response("Senha deve ter pelo menos 6 caracteres", 400)
            user.set_password(data['password'])
        
        db.session.commit()
        
        return success_response(
            data=user.to_dict(),
            message="Perfil atualizado com sucesso"
        )
    
    except Exception as e:
        db.session.rollback()
        return error_response(f"Erro ao atualizar perfil: {str(e)}", 500)
