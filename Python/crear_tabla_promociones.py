#!/usr/bin/env python3
"""
Script para crear la tabla de promociones en la base de datos Molpi
"""

import sqlite3
import os
from datetime import datetime

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

def crear_tabla_promociones():
    """Crear la tabla promociones si no existe"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear tabla promociones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS promociones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            imagen TEXT NOT NULL,
            orden INTEGER DEFAULT 0,
            activo BOOLEAN DEFAULT 1,
            fecha_inicio DATE,
            fecha_fin DATE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    print("✅ Tabla 'promociones' creada correctamente")
    
    # Verificar si ya hay promociones
    cursor.execute("SELECT COUNT(*) FROM promociones")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("📝 Agregando promoción de ejemplo...")
        
        # Insertar promoción de ejemplo
        cursor.execute('''
            INSERT INTO promociones (titulo, imagen, orden, activo, fecha_inicio, fecha_fin)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            "¡Oferta Especial en Moldes!",
            "img/promocion-ejemplo.jpg", 
            1,
            1,
            "2025-01-01",
            "2025-12-31"
        ))
        
        print("✅ Promoción de ejemplo agregada")
    else:
        print(f"ℹ️ Ya existen {count} promociones en la base de datos")
    
    conn.commit()
    conn.close()
    
    print("🎯 Tabla de promociones lista para usar")

if __name__ == "__main__":
    print("🚀 Creando tabla de promociones...")
    crear_tabla_promociones()
    print("✨ ¡Proceso completado!")
