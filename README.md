# Vivace Backend

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask Version](https://img.shields.io/badge/flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📖 Descrição

O **Vivace Backend** é uma API RESTful desenvolvida em Flask que serve como backend para o sistema Vivace. Esta aplicação fornece uma solução completa para gerenciamento de receitas culinárias, ingredientes, empresas e categorias, com sistema robusto de autenticação e autorização.

## ✨ Funcionalidades

- 🔐 **Autenticação Segura**: Sistema de login com hash de senhas e tokens JWT
- 📝 **CRUD Completo**: Operações completas para todas as entidades
- 🗃️ **Gerenciamento de Dados**: Migrations e seeders para estrutura do banco
- 🔒 **Autorização**: Sistema baseado em tokens para controle de acesso
- 📊 **Estrutura Modular**: Organização clara em módulos e rotas

## 🚀 Tecnologias Utilizadas

- **[Python 3.8+](https://www.python.org/)** - Linguagem de programação
- **[Flask](https://flask.palletsprojects.com/)** - Framework web
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM para banco de dados
- **[Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)** - Gerenciamento de tokens JWT
- **[Flask-Migrate](https://flask-migrate.readthedocs.io/)** - Migrações do banco de dados
- **[Werkzeug](https://werkzeug.palletsprojects.com/)** - Hash de senhas
- **[python-dotenv](https://pypi.org/project/python-dotenv/)** - Gerenciamento de variáveis de ambiente

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Banco de dados (SQLite, PostgreSQL, MySQL)

## 🛠️ Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/GeovaneFernandes/Vivace-Backend.git
   cd Vivace-Backend
   ```

2. **Crie um ambiente virtual**

   ```bash
   python -m venv venv

   # No Windows
   venv\Scripts\activate

   # No Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**

   ```bash
   # Copie o arquivo de exemplo
   cp .env.example .env

   # Edite o arquivo .env com suas configurações
   ```

5. **Execute as migrações**

   ```bash
   flask db upgrade
   ```

6. **Execute os seeders (opcional)**
   ```bash
   python seeders/run_seeders.py
   ```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_super_segura

# Configurações do Banco de Dados
DATABASE_URL=sqlite:///vivace.db

# Configurações JWT
JWT_SECRET_KEY=sua_chave_jwt_super_secreta
JWT_ACCESS_TOKEN_EXPIRES=3600

# Outras configurações
DEBUG=True
```

## 🚀 Uso

Para iniciar o servidor de desenvolvimento:

```bash
flask run
```

A API estará disponível em `http://localhost:5000`

## 📚 Documentação da API

### 🔐 Autenticação

#### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

#### Registro

```http
POST /auth/register
Content-Type: application/json

{
  "name": "Nome do Usuário",
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

### 🥕 Ingredientes

| Método   | Endpoint                | Descrição                    |
| -------- | ----------------------- | ---------------------------- |
| `GET`    | `/api/ingredients`      | Listar todos os ingredientes |
| `GET`    | `/api/ingredients/{id}` | Obter ingrediente específico |
| `POST`   | `/api/ingredients`      | Criar novo ingrediente       |
| `PUT`    | `/api/ingredients/{id}` | Atualizar ingrediente        |
| `DELETE` | `/api/ingredients/{id}` | Deletar ingrediente          |

### 📝 Receitas

| Método   | Endpoint            | Descrição                |
| -------- | ------------------- | ------------------------ |
| `GET`    | `/api/recipes`      | Listar todas as receitas |
| `GET`    | `/api/recipes/{id}` | Obter receita específica |
| `POST`   | `/api/recipes`      | Criar nova receita       |
| `PUT`    | `/api/recipes/{id}` | Atualizar receita        |
| `DELETE` | `/api/recipes/{id}` | Deletar receita          |

### 🏢 Empresas

| Método   | Endpoint              | Descrição                |
| -------- | --------------------- | ------------------------ |
| `GET`    | `/api/companies`      | Listar todas as empresas |
| `GET`    | `/api/companies/{id}` | Obter empresa específica |
| `POST`   | `/api/companies`      | Criar nova empresa       |
| `PUT`    | `/api/companies/{id}` | Atualizar empresa        |
| `DELETE` | `/api/companies/{id}` | Deletar empresa          |

### 📂 Categorias

| Método   | Endpoint               | Descrição                  |
| -------- | ---------------------- | -------------------------- |
| `GET`    | `/api/categories`      | Listar todas as categorias |
| `GET`    | `/api/categories/{id}` | Obter categoria específica |
| `POST`   | `/api/categories`      | Criar nova categoria       |
| `PUT`    | `/api/categories/{id}` | Atualizar categoria        |
| `DELETE` | `/api/categories/{id}` | Deletar categoria          |

## 📁 Estrutura do Projeto

```
Vivace-Backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   ├── company.py
│   │   └── category.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── ingredients.py
│   │   ├── recipes.py
│   │   ├── companies.py
│   │   └── categories.py
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       └── helpers.py
├── migrations/
├── seeders/
│   ├── __init__.py
│   ├── ingredient_seeder.py
│   ├── category_seeder.py
│   └── run_seeders.py
├── tests/
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## 🧪 Testes

Para executar os testes:

```bash
# Executar todos os testes
python -m pytest

# Executar com cobertura
python -m pytest --cov=app

# Executar testes específicos
python -m pytest tests/test_auth.py
```

## 🚀 Deploy

### Usando Heroku

1. **Instale o Heroku CLI**
2. **Faça login no Heroku**

   ```bash
   heroku login
   ```

3. **Crie uma aplicação**

   ```bash
   heroku create vivace-backend
   ```

4. **Configure as variáveis de ambiente**

   ```bash
   heroku config:set SECRET_KEY=sua_chave_secreta
   heroku config:set DATABASE_URL=postgresql://...
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

### Usando Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Geovane Fernandes** - _Desenvolvedor Principal_ - [@GeovaneFernandes](https://github.com/GeovaneFernandes)

## 📞 Contato

- GitHub: [@GeovaneFernandes](https://github.com/GeovaneFernandes)
- Email: [seu.email@exemplo.com](mailto:seu.email@exemplo.com)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- Flask Community
- Todos os contribuidores que ajudaram neste projeto
- Inspiração para criar uma solução completa de gerenciamento culinário

---

<p align="center">Feito com ❤️ por <a href="https://github.com/GeovaneFernandes">Geovane Fernandes</a></p>
