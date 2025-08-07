#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def mostrar_productos_50x50():
    """
    Muestra todos los productos actuales en la línea 50x50
    """
    
    db_path = "molpi.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, nombre, imagen_url 
            FROM productos 
            WHERE subcategoria = 'Línea 50x50' 
            ORDER BY id
        """)
        
        productos = cursor.fetchall()
        
        print("=== PRODUCTOS ACTUALES EN LÍNEA 50x50 ===")
        print(f"Total: {len(productos)} productos\n")
        
        for id_prod, nombre, imagen_url in productos:
            print(f"ID: {id_prod:3d} | {nombre:40s} | {imagen_url}")
        
        conn.close()
        
        # Productos que deberían quedarse según las imágenes mostradas
        productos_correctos = [
            "Quebracho",
            "Corteza", 
            "Madera 50x25x6 / 2 piezas por molde",
            "Liso",
            "Deck Símil Madera",
            "Deck Antideslizante", 
            "Laja San Juan",
            "Adoquín Colonial"
        ]
        
        print(f"\n=== PRODUCTOS QUE DEBERÍAN QUEDARSE (8 productos) ===")
        for i, nombre in enumerate(productos_correctos, 1):
            print(f"{i}. {nombre}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    mostrar_productos_50x50()
