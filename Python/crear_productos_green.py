#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def agregar_productos_green():
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar', 'instance', 'molpi.db')
    
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en {db_path}")
        return
    
    print(f"📁 Usando base de datos: {db_path}")
    
    # Productos Green a agregar
    productos_green = [
        {
            'nombre': 'Rombo Green',
            'categoria': 'Green',
            'subcategoria': 'Grama Sintética',
            'descripcion': 'Molde con forma de rombo especialmente diseñado para superficies con grama sintética. Proporciona una textura única y atractiva.',
            'imagen_url': 'img/products/rombo_green_molde.jpg',
            'imagen_mosaico_url': 'img/products/rombo_green_mosaico.png',
            'precio': 0,
            'precio_usd': 0,
            'pdf_url': '',
            'activo': 1
        },
        {
            'nombre': 'Círculos Green',
            'categoria': 'Green',
            'subcategoria': 'Grama Sintética',
            'descripcion': 'Molde con círculos diseñado para grama sintética. Ideal para espacios deportivos y recreativos.',
            'imagen_url': 'img/products/circulos_green_molde.jpg',
            'imagen_mosaico_url': 'img/products/circulos_green_mosaico.png',
            'precio': 0,
            'precio_usd': 0,
            'pdf_url': '',
            'activo': 1
        },
        {
            'nombre': 'Recto Green',
            'categoria': 'Green',
            'subcategoria': 'Grama Sintética',
            'descripcion': 'Molde con diseño recto para grama sintética. Perfecto para crear superficies uniformes y funcionales.',
            'imagen_url': 'img/products/recto_green_molde.jpg',
            'imagen_mosaico_url': 'img/products/recto_green_mosaico.png',
            'precio': 0,
            'precio_usd': 0,
            'pdf_url': '',
            'activo': 1
        },
        {
            'nombre': 'Adoquín Individual',
            'categoria': 'Green',
            'subcategoria': 'Adoquinado',
            'descripcion': 'Molde para adoquín individual con aplicación en espacios verdes. Combina funcionalidad y estética.',
            'imagen_url': 'img/products/adoquin_individual_molde.jpg',
            'imagen_mosaico_url': 'img/products/adoquin_individual_mosaico.png',
            'precio': 0,
            'precio_usd': 0,
            'pdf_url': '',
            'activo': 1
        },
        {
            'nombre': 'Intertrabado',
            'categoria': 'Green',
            'subcategoria': 'Pavimentación',
            'descripcion': 'Sistema de pavimentación intertrabado ideal para áreas verdes y espacios exteriores que requieren drenaje.',
            'imagen_url': 'img/products/intertrabado.jpg',
            'imagen_mosaico_url': 'img/products/intertrabado_mosaico.png',
            'precio': 0,
            'precio_usd': 0,
            'pdf_url': '',
            'activo': 1
        }
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🟢 Agregando productos Green...")
    
    for producto in productos_green:
        try:
            # Verificar si el producto ya existe
            cursor.execute("""
                SELECT id FROM productos 
                WHERE nombre = ? AND categoria = ?
            """, (producto['nombre'], producto['categoria']))
            
            existe = cursor.fetchone()
            
            if existe:
                print(f"⚠️  El producto '{producto['nombre']}' ya existe (ID: {existe[0]})")
                continue
            
            # Insertar el producto
            cursor.execute("""
                INSERT INTO productos (
                    nombre, categoria, subcategoria, descripcion, 
                    imagen_url, imagen_mosaico_url, precio, precio_usd, 
                    pdf_url, activo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                producto['nombre'],
                producto['categoria'],
                producto['subcategoria'],
                producto['descripcion'],
                producto['imagen_url'],
                producto['imagen_mosaico_url'],
                producto['precio'],
                producto['precio_usd'],
                producto['pdf_url'],
                producto['activo']
            ))
            
            product_id = cursor.lastrowid
            print(f"✅ Producto '{producto['nombre']}' agregado con ID: {product_id}")
            
        except Exception as e:
            print(f"❌ Error al agregar '{producto['nombre']}': {e}")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Proceso completado!")
    print("\n📋 Verificando productos Green creados...")
    
    # Verificar productos creados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, categoria, subcategoria, activo
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY id DESC
    """)
    
    productos = cursor.fetchall()
    
    if productos:
        print("\n🟢 Productos Green en la base de datos:")
        for producto in productos:
            estado = "✅ Activo" if producto[4] == 1 else "❌ Inactivo"
            print(f"  ID: {producto[0]} | {producto[1]} | {producto[2]} | {producto[3]} | {estado}")
    else:
        print("❌ No se encontraron productos Green")
    
    conn.close()

if __name__ == "__main__":
    agregar_productos_green()
