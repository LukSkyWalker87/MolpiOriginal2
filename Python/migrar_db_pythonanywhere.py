#!/usr/bin/env python3
"""
Script para ejecutar migraciones en PythonAnywhere
Subir a /home/sgit/mysite/ y ejecutar: python migrar_db_pythonanywhere.py
"""

import sqlite3
import os
from datetime import datetime

def ejecutar_migraciones():
    """Ejecutar las migraciones necesarias en la base de datos"""
    
    print("🔧 EJECUTANDO MIGRACIONES EN PYTHONANYWHERE")
    print("=" * 50)
    
    db_path = 'molpi.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        print(f"✅ Conectado a: {db_path}")
        print(f"📊 Tamaño: {os.path.getsize(db_path):,} bytes")
        
        # Verificar tablas existentes
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = [row[0] for row in c.fetchall()]
        print(f"📋 Tablas: {', '.join(tablas)}")
        
        # Función para agregar columna si no existe
        def agregar_columna(tabla, columna, tipo, default=None):
            try:
                # Verificar si la columna ya existe
                c.execute(f"PRAGMA table_info({tabla})")
                columnas_existentes = [row[1] for row in c.fetchall()]
                
                if columna not in columnas_existentes:
                    if default:
                        c.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo} DEFAULT {default}")
                    else:
                        c.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")
                    print(f"✅ Agregada columna {tabla}.{columna}")
                    return True
                else:
                    print(f"ℹ️ Columna {tabla}.{columna} ya existe")
                    return False
            except Exception as e:
                print(f"❌ Error agregando {tabla}.{columna}: {e}")
                return False
        
        # MIGRACIONES ESPECÍFICAS
        print("\n🔧 Aplicando migraciones...")
        
        cambios = 0
        
        # Productos: agregar columnas faltantes
        if 'productos' in tablas:
            cambios += agregar_columna('productos', 'imagen_mosaico_url', 'TEXT', "''")
            cambios += agregar_columna('productos', 'precio_usd', 'REAL', '0.0')
            cambios += agregar_columna('productos', 'fecha_creacion', 'DATETIME', 'CURRENT_TIMESTAMP')
            cambios += agregar_columna('productos', 'fecha_modificacion', 'DATETIME', 'CURRENT_TIMESTAMP')
        
        # Categorías: agregar columnas faltantes
        if 'categorias' in tablas:
            cambios += agregar_columna('categorias', 'activo', 'INTEGER', '1')
            cambios += agregar_columna('categorias', 'descripcion', 'TEXT', "''")
        
        # Subcategorías: agregar columnas faltantes
        if 'subcategorias' in tablas:
            cambios += agregar_columna('subcategorias', 'activo', 'INTEGER', '1')
            cambios += agregar_columna('subcategorias', 'descripcion', 'TEXT', "''")
        
        # Promociones: agregar columnas faltantes
        if 'promociones' in tablas:
            cambios += agregar_columna('promociones', 'cartilla_pdf', 'TEXT', "''")
            cambios += agregar_columna('promociones', 'fecha_inicio', 'DATE', 'NULL')
            cambios += agregar_columna('promociones', 'fecha_fin', 'DATE', 'NULL')
            cambios += agregar_columna('promociones', 'fecha_creacion', 'DATETIME', 'CURRENT_TIMESTAMP')
            cambios += agregar_columna('promociones', 'fecha_modificacion', 'DATETIME', 'CURRENT_TIMESTAMP')
        
        # Testimonios: agregar columnas faltantes
        if 'testimonios' in tablas:
            cambios += agregar_columna('testimonios', 'empresa', 'TEXT', "''")
            cambios += agregar_columna('testimonios', 'orden', 'INTEGER', '1')
            cambios += agregar_columna('testimonios', 'fecha_creacion', 'DATETIME', 'CURRENT_TIMESTAMP')
            cambios += agregar_columna('testimonios', 'fecha_modificacion', 'DATETIME', 'CURRENT_TIMESTAMP')
        
        # Commit cambios
        conn.commit()
        
        # Verificar datos después de migraciones
        print(f"\n📊 VERIFICACIÓN POST-MIGRACIÓN:")
        
        for tabla in ['productos', 'categorias', 'subcategorias', 'promociones', 'testimonios']:
            if tabla in tablas:
                c.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = c.fetchone()[0]
                print(f"  {tabla}: {count} registros")
                
                # Mostrar primeros registros
                if count > 0:
                    if tabla == 'productos':
                        c.execute("SELECT id, nombre, categoria FROM productos LIMIT 3")
                    elif tabla == 'categorias':
                        c.execute("SELECT id, nombre FROM categorias LIMIT 3")
                    else:
                        c.execute(f"SELECT * FROM {tabla} LIMIT 1")
                    
                    sample = c.fetchall()
                    for row in sample:
                        print(f"    • {row[:3]}...")
        
        conn.close()
        
        print(f"\n✅ MIGRACIONES COMPLETADAS")
        print(f"📝 Cambios aplicados: {cambios}")
        print(f"🕒 Fecha: {datetime.now()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando migraciones: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    ejecutar_migraciones()
