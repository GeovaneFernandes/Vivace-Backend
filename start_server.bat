@echo off
echo 🚀 Iniciando servidor Vivace Backend...
echo.
echo ✅ Servidor disponível em: http://localhost:5000
echo 🔑 Health Check: http://localhost:5000
echo 📚 Usuários de teste:
echo    - admin@vivace.com (senha: admin123)
echo    - chef@vivace.com (senha: chef123)  
echo    - user@vivace.com (senha: user123)
echo.
echo 💡 Pressione Ctrl+C para parar o servidor
echo.

"%~dp0.venv\Scripts\python.exe" "%~dp0app.py"

echo.
echo 👋 Servidor encerrado!
pause
