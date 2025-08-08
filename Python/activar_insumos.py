#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def main():
    # Conectar a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("🔧 Activando productos de insumos...")

    # Activar todos los productos de insumos
    cursor.execute("""
        UPDATE productos 
        SET activo = 1 
        WHERE categoria = 'Insumos'
    """)

    rows_affected = cursor.rowcount
    print(f"✅ Productos de insumos activados: {rows_affected}")

    # Confirmar cambios
    conn.commit()

    # Verificar el estado actual por subcategoría
    cursor.execute("""
        SELECT subcategoria, COUNT(*) as total, 
               SUM(CASE WHEN activo = 1 THEN 1 ELSE 0 END) as activos
        FROM productos 
        WHERE categoria = 'Insumos'
        GROUP BY subcategoria
        ORDER BY subcategoria
    """)

    results = cursor.fetchall()
    print("\n📊 Estado actual de productos de insumos por subcategoría:")
    
    for subcategoria, total, activos in results:
        print(f"  • {subcategoria}: {activos}/{total} activos")

    # Mostrar productos específicos de curadores
    cursor.execute("""
        SELECT nombre, activo FROM productos 
        WHERE categoria = 'Insumos' AND subcategoria = 'Curadores'
        ORDER BY nombre
    """)

    curadores = cursor.fetchall()
    print("\n🧪 Estado de productos Curadores:")
    for nombre, activo in curadores:
        status = "ACTIVO" if activo else "INACTIVO"
        print(f"  - {nombre}: {status}")

    conn.close()
    print("\n✅ ¡Actualización completada!")

if __name__ == "__main__":
    main()
