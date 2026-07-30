"""
Script de migración para actualizar la base de datos con las nuevas columnas.
"""
import os
import sqlite3
from datetime import datetime

DB_PATH = 'enlaces.db'

def migrate_database():
    """Migra la base de datos a la nueva estructura."""

    print("🔧 Iniciando migración de base de datos...")

    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verificar qué columnas existen en categorias
        cursor.execute("PRAGMA table_info(categorias)")
        categorias_columns = [col[1] for col in cursor.fetchall()]

        # Agregar columnas faltantes en categorias
        if 'icono' not in categorias_columns:
            print("  ➕ Agregando columna 'icono' a categorias...")
            cursor.execute("ALTER TABLE categorias ADD COLUMN icono VARCHAR(50) DEFAULT '📁'")
            cursor.execute("UPDATE categorias SET icono = '📁' WHERE icono IS NULL")

        if 'color' not in categorias_columns:
            print("  ➕ Agregando columna 'color' a categorias...")
            cursor.execute("ALTER TABLE categorias ADD COLUMN color VARCHAR(7) DEFAULT '#667eea'")
            cursor.execute("UPDATE categorias SET color = '#667eea' WHERE color IS NULL")

        # Verificar qué columnas existen en enlaces
        cursor.execute("PRAGMA table_info(enlaces)")
        enlaces_columns = [col[1] for col in cursor.fetchall()]

        # Agregar columnas faltantes en enlaces
        if 'descripcion' not in enlaces_columns:
            print("  ➕ Agregando columna 'descripcion' a enlaces...")
            cursor.execute("ALTER TABLE enlaces ADD COLUMN descripcion TEXT DEFAULT ''")

        if 'favorito' not in enlaces_columns:
            print("  ➕ Agregando columna 'favorito' a enlaces...")
            cursor.execute("ALTER TABLE enlaces ADD COLUMN favorito BOOLEAN DEFAULT 0")

        if 'clicks' not in enlaces_columns:
            print("  ➕ Agregando columna 'clicks' a enlaces...")
            cursor.execute("ALTER TABLE enlaces ADD COLUMN clicks INTEGER DEFAULT 0")

        if 'tags' not in enlaces_columns:
            print("  ➕ Agregando columna 'tags' a enlaces...")
            cursor.execute("ALTER TABLE enlaces ADD COLUMN tags VARCHAR(200) DEFAULT ''")

        if 'fecha_ultimo_acceso' not in enlaces_columns:
            print("  ➕ Agregando columna 'fecha_ultimo_acceso' a enlaces...")
            cursor.execute("ALTER TABLE enlaces ADD COLUMN fecha_ultimo_acceso DATETIME")

        conn.commit()
        print("✅ Migración completada exitosamente!")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error durante la migración: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    if os.path.exists(DB_PATH):
        print(f"📁 Base de datos encontrada: {DB_PATH}")
        migrate_database()
    else:
        print(f"⚠️  Base de datos no encontrada en {DB_PATH}")
        print("La base de datos se creará automáticamente al iniciar la aplicación.")
