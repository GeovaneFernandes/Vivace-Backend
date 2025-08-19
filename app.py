from app import create_app
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Cria a aplicação Flask
app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
