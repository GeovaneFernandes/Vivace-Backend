import json
from app.models.user import User
from app import db

def test_health_check(client):
    """Testa o endpoint de health check"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_user_registration(client):
    """Testa o registro de usuário"""
    user_data = {
        'name': 'Usuário Teste',
        'email': 'teste@exemplo.com',
        'password': 'senha123'
    }
    
    response = client.post('/auth/register', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert data['data']['email'] == user_data['email']

def test_user_registration_invalid_email(client):
    """Testa registro com email inválido"""
    user_data = {
        'name': 'Usuário Teste',
        'email': 'email-invalido',
        'password': 'senha123'
    }
    
    response = client.post('/auth/register', 
                          data=json.dumps(user_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['success'] is False

def test_user_login(client):
    """Testa o login do usuário"""
    # Primeiro registra um usuário
    user = User(
        name='Usuário Teste',
        email='teste@exemplo.com',
        password='senha123'
    )
    db.session.add(user)
    db.session.commit()
    
    # Tenta fazer login
    login_data = {
        'email': 'teste@exemplo.com',
        'password': 'senha123'
    }
    
    response = client.post('/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'access_token' in data['data']

def test_user_login_invalid_credentials(client):
    """Testa login com credenciais inválidas"""
    login_data = {
        'email': 'inexistente@exemplo.com',
        'password': 'senhaerrada'
    }
    
    response = client.post('/auth/login',
                          data=json.dumps(login_data),
                          content_type='application/json')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
