#!/usr/bin/env python3
"""Script para agregar el campo imagen_mosaico_url a la tabla productos"""

import sqlite3
import os

def agregar_campo_mosaico():
    """Agregar el campo imagen_mosaico_url a la tabla productos si no existe"""
    
    db_path = 'molpi.db'
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Verificar si el campo ya existe
        c.execute("PRAGMA table_info(productos)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'imagen_mosaico_url' in columns:
            print("✅ El campo imagen_mosaico_url ya existe en la tabla productos")
            conn.close()
            return True
        
        # Agregar el nuevo campo
        print("🔧 Agregando campo imagen_mosaico_url a la tabla productos...")
        c.execute("ALTER TABLE productos ADD COLUMN imagen_mosaico_url TEXT")
        
        conn.commit()
        conn.close()
        
        print("✅ Campo imagen_mosaico_url agregado exitosamente")
        
        # Verificar que se agregó correctamente
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("PRAGMA table_info(productos)")
        columns_after = [column[1] for column in c.fetchall()]
        conn.close()
        
        print(f"📋 Campos actuales: {columns_after}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al agregar el campo: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Agregando campo imagen_mosaico_url ===")
    success = agregar_campo_mosaico()
    if success:
        print("🎉 ¡Proceso completado exitosamente!")
    else:
        print("💥 Proceso falló")
