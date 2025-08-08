#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json

def test_productos_piscinas():
    """
    Probar la funcionalidad del endpoint de piscinas directamente con la base de datos
    """
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('molpi.db')
        cursor = conn.cursor()
        
        # Misma consulta que el endpoint
        cursor.execute("""
            SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
                   precio, precio_usd, activo, fecha_creacion, fecha_modificacion
            FROM productos 
            WHERE activo = 1 AND categoria = 'Piscinas'
            ORDER BY subcategoria, nombre
        """)
        rows = cursor.fetchall()
        conn.close()
        
        # Organizar productos por subcategoría
        productos_por_subcategoria = {}
        
        for row in rows:
            producto = {
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2],
                'pdf_url': row[3],
                'imagen_url': row[4],
                'imagen_mosaico_url': row[5],
                'categoria': row[6],
                'subcategoria': row[7],
                'precio': row[8],
                'precio_usd': row[9],
                'activo': row[10],
                'fecha_creacion': row[11],
                'fecha_modificacion': row[12]
            }
            
            subcategoria = producto['subcategoria']
            if subcategoria not in productos_por_subcategoria:
                productos_por_subcategoria[subcategoria] = []
            
            productos_por_subcategoria[subcategoria].append(producto)
        
        print("✅ Simulación del endpoint /productos/piscinas")
        print("="*60)
        
        if productos_por_subcategoria:
            print(f"Subcategorías encontradas: {list(productos_por_subcategoria.keys())}")
            print()
            
            for subcategoria, productos_sub in productos_por_subcategoria.items():
                print(f"{subcategoria}: {len(productos_sub)} productos")
                for producto in productos_sub:
                    print(f"  - {producto['nombre']} (${producto['precio']}) - {producto['imagen_url']}")
                print()
            
            # Crear archivo JSON para verificar estructura
            with open('test_piscinas_response.json', 'w', encoding='utf-8') as f:
                json.dump(productos_por_subcategoria, f, indent=2, ensure_ascii=False)
            print("💾 Respuesta guardada en: test_piscinas_response.json")
            
        else:
            print("❌ No se encontraron productos en la categoría Piscinas")
            
        return productos_por_subcategoria
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_productos_piscinas()
