from flask import jsonify
import re

def success_response(data=None, message="Operação realizada com sucesso", status_code=200):
    """Padroniza respostas de sucesso"""
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="Erro interno do servidor", status_code=500, errors=None):
    """Padroniza respostas de erro"""
    response = {"success": False, "message": message}
    if errors:
        response["errors"] = errors
    return jsonify(response), status_code

def validate_email(email):
    """Valida formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def paginate_query(query, page=1, per_page=10):
    """Aplica paginação a uma query"""
    try:
        paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        return {
            'items': [item.to_dict() for item in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    except Exception as e:
        return None
