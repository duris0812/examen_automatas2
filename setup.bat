@echo off
echo Iniciando configuracion del proyecto...

echo.
echo [1] Creando migraciones...
python manage.py migrate

echo.
echo [2] Proyecto listo! 
echo.
echo Para iniciar el servidor ejecuta:
echo    python manage.py runserver
echo.
echo Luego abre tu navegador en:
echo    http://127.0.0.1:8000/
echo.
pause
