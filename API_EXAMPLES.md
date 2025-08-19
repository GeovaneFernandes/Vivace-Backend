# Exemplos de Uso da API Vivace Backend

Este documento contém exemplos práticos de como usar a API Vivace Backend.

## 🔐 Autenticação

### 1. Registrar um novo usuário

```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@exemplo.com",
    "password": "senha123"
  }'
```

### 2. Fazer login

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@vivace.com",
    "password": "admin123"
  }'
```

**Resposta:**

```json
{
  "success": true,
  "message": "Login realizado com sucesso",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "name": "Administrador",
      "email": "admin@vivace.com",
      "is_active": true
    }
  }
}
```

### 3. Obter perfil do usuário

```bash
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 🥕 Ingredientes

### 1. Listar ingredientes

```bash
curl -X GET http://localhost:5000/api/ingredients
```

### 2. Buscar ingredientes com paginação

```bash
curl -X GET "http://localhost:5000/api/ingredients?page=1&per_page=5&search=tomate"
```

### 3. Criar novo ingrediente

```bash
curl -X POST http://localhost:5000/api/ingredients \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Abacate",
    "description": "Abacate maduro",
    "unit_of_measure": "unidade",
    "price_per_unit": 3.50
  }'
```

### 4. Atualizar ingrediente

```bash
curl -X PUT http://localhost:5000/api/ingredients/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Tomate Cherry",
    "description": "Tomate cherry orgânico",
    "price_per_unit": 12.99
  }'
```

### 5. Deletar ingrediente

```bash
curl -X DELETE http://localhost:5000/api/ingredients/1 \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📂 Categorias

### 1. Listar categorias

```bash
curl -X GET http://localhost:5000/api/categories
```

### 2. Criar nova categoria

```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Comida Japonesa",
    "description": "Pratos da culinária japonesa"
  }'
```

## 🏢 Empresas

### 1. Listar empresas

```bash
curl -X GET http://localhost:5000/api/companies
```

### 2. Criar nova empresa

```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Meu Restaurante",
    "description": "Restaurante familiar",
    "email": "contato@meurestaurante.com",
    "phone": "(11) 9999-8888",
    "address": "Rua das Palmeiras, 456",
    "city": "São Paulo",
    "state": "SP",
    "website": "https://meurestaurante.com"
  }'
```

## 📝 Receitas

### 1. Listar receitas

```bash
curl -X GET http://localhost:5000/api/recipes
```

### 2. Buscar receitas por categoria

```bash
curl -X GET "http://localhost:5000/api/recipes?category_id=1"
```

### 3. Obter receita específica com ingredientes

```bash
curl -X GET http://localhost:5000/api/recipes/1
```

### 4. Criar nova receita

```bash
curl -X POST http://localhost:5000/api/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Salada Caesar",
    "description": "Salada Caesar clássica",
    "instructions": "1. Misture os ingredientes\n2. Sirva gelado",
    "prep_time": 15,
    "servings": 2,
    "difficulty_level": "easy",
    "category_id": 6,
    "company_id": 1,
    "ingredients": [
      {
        "ingredient_id": 4,
        "quantity": 200,
        "unit": "g"
      },
      {
        "ingredient_id": 16,
        "quantity": 50,
        "unit": "g"
      }
    ]
  }'
```

### 5. Atualizar receita

```bash
curl -X PUT http://localhost:5000/api/recipes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "name": "Salada Caesar Premium",
    "prep_time": 20,
    "servings": 4
  }'
```

## 🧪 Testando com Python

```python
import requests
import json

# URL base da API
BASE_URL = "http://localhost:5000"

# 1. Fazer login
login_data = {
    "email": "admin@vivace.com",
    "password": "admin123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
token = response.json()["data"]["access_token"]

# Headers com token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Listar ingredientes
ingredients = requests.get(f"{BASE_URL}/api/ingredients").json()
print("Ingredientes:", json.dumps(ingredients, indent=2))

# 3. Criar novo ingrediente
new_ingredient = {
    "name": "Azeite de Oliva Premium",
    "description": "Azeite extra virgem importado",
    "unit_of_measure": "ml",
    "price_per_unit": 0.08
}

response = requests.post(f"{BASE_URL}/api/ingredients", json=new_ingredient, headers=headers)
print("Novo ingrediente:", json.dumps(response.json(), indent=2))
```

## 🔧 Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Dados inválidos
- `401` - Não autorizado
- `403` - Acesso negado
- `404` - Não encontrado
- `500` - Erro interno do servidor

## 🌟 Dicas

1. **Token JWT**: Todos os endpoints que requerem autenticação precisam do header `Authorization: Bearer TOKEN`

2. **Paginação**: Use os parâmetros `page` e `per_page` para controlar a paginação

3. **Busca**: Use o parâmetro `search` para filtrar resultados

4. **Soft Delete**: Itens deletados são marcados como inativos, não removidos permanentemente

5. **Validação**: A API sempre retorna mensagens de erro descritivas para facilitar o debug
