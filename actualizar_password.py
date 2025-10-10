#!/usr/bin/env python3
"""
Script para actualizar la contraseña del usuario admin en la base de datos
"""
import sqlite3
import sys
from pathlib import Path

# Ruta a la base de datos
DB_PATH = Path(__file__).parent / 'backend' / 'molpi.db'

def update_admin_password(new_password):
    """Actualiza la contraseña del usuario admin"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Primero verificar si existe la tabla users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
            if not cursor.fetchone():
                print("❌ No se encontró tabla 'users' ni 'user'")
                print("\n📋 Tablas disponibles:")
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                for table in cursor.fetchall():
                    print(f"   - {table[0]}")
                return False
            table_name = 'user'
        else:
            table_name = 'users'
        
        # Ver estructura de la tabla
        print(f"\n📋 Estructura de la tabla '{table_name}':")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
        
        # Ver usuarios actuales
        print(f"\n👥 Usuarios actuales:")
        cursor.execute(f"SELECT * FROM {table_name}")
        users = cursor.fetchall()
        for user in users:
            print(f"   {user}")
        
        # Actualizar contraseña
        print(f"\n🔄 Actualizando contraseña...")
        cursor.execute(f"UPDATE {table_name} SET password = ? WHERE username = 'admin'", (new_password,))
        
        if cursor.rowcount == 0:
            print("⚠️  No se encontró usuario 'admin', intentando insertar...")
            cursor.execute(f"INSERT INTO {table_name} (username, password) VALUES ('admin', ?)", (new_password,))
        
        conn.commit()
        print(f"✅ Contraseña actualizada exitosamente")
        
        # Verificar
        cursor.execute(f"SELECT username, password FROM {table_name} WHERE username = 'admin'")
        result = cursor.fetchone()
        print(f"\n✓ Usuario: {result[0]}")
        print(f"✓ Contraseña: {result[1]}")
        
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🔐 ACTUALIZAR CONTRASEÑA DE ADMIN")
    print("=" * 70)
    
    nueva_password = "dumba3110"
    
    if update_admin_password(nueva_password):
        print("\n" + "=" * 70)
        print("✅ Proceso completado")
        print("=" * 70)
        print(f"\n🔑 Nuevas credenciales:")
        print(f"   Usuario: admin")
        print(f"   Contraseña: {nueva_password}")
        print("\n🌐 Prueba en: https://molpi.com.ar/admin")
    else:
        print("\n❌ Error al actualizar contraseña")
        sys.exit(1)
