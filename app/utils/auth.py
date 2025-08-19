from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

def token_required(f):
    """Decorator para rotas que requerem autenticação"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user or not current_user.is_active:
                return jsonify({'message': 'Token inválido ou usuário inativo'}), 401
            
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token inválido', 'error': str(e)}), 401
    
    return decorated_function

def validate_user_data(data, required_fields):
    """Valida se os campos obrigatórios estão presentes nos dados"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Campos obrigatórios não informados: {', '.join(missing_fields)}"
    
    return True, None
