#!/usr/bin/env python3
"""
Script para ejecutar la aplicación en desarrollo con variables de entorno desde .env
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Verificar credenciales
print("\n" + "=" * 60)
print("🔐 VERIFICACIÓN DE CREDENCIALES")
print("=" * 60)
print(f"SECRET_KEY: {'✅ Configurada' if os.getenv('SECRET_KEY') else '❌ NO CONFIGURADA'}")
print(f"GOOGLE_CLIENT_ID: {'✅ ' + os.getenv('GOOGLE_CLIENT_ID')[:50] + '...' if os.getenv('GOOGLE_CLIENT_ID') else '❌ NO CONFIGURADA'}")
print(f"GOOGLE_CLIENT_SECRET: {'✅ Configurada' if os.getenv('GOOGLE_CLIENT_SECRET') else '❌ NO CONFIGURADA'}")
print("=" * 60 + "\n")

# Importar y ejecutar la app
from app import app, init_db

if __name__ == '__main__':
    # Inicializar la base de datos
    init_db(app)

    # Ejecutar la aplicación
    print("\n" + "=" * 60)
    print("🚀 APLICACIÓN DE GESTIÓN DE ENLACES (CON OAUTH)")
    print("=" * 60)
    print("📍 Abre tu navegador en: http://localhost:5000")
    print("🔐 Click en 'Iniciar con Google' para autenticarte")
    print("🛑 Presiona Ctrl+C para detener el servidor")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
