#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

def conectar_db():
    """Conecta a la base de datos"""
    db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    return sqlite3.connect(db_path)

def insertar_o_actualizar_producto(conn, producto_data):
    """Inserta un nuevo producto o actualiza uno existente"""
    cursor = conn.cursor()
    
    # Verificar si el producto ya existe por nombre
    cursor.execute("SELECT id FROM productos WHERE nombre = ?", (producto_data['nombre'],))
    producto_existente = cursor.fetchone()
    
    if producto_existente:
        # Actualizar producto existente
        producto_id = producto_existente[0]
        cursor.execute("""
            UPDATE productos SET 
                categoria = ?, subcategoria = ?, precio = ?, precio_usd = ?, 
                imagen_url = ?, imagen_mosaico_url = ?, descripcion = ?, activo = 1
            WHERE id = ?
        """, (producto_data['categoria'], producto_data['subcategoria'], 
              producto_data['precio'], producto_data['precio_usd'], 
              producto_data['imagen_url'], producto_data['imagen_mosaico_url'], 
              producto_data['descripcion'], producto_id))
        
        print(f"✅ Producto actualizado: {producto_data['nombre']}")
        return producto_id, False
    else:
        # Insertar nuevo producto
        cursor.execute("""
            INSERT INTO productos (nombre, categoria, subcategoria, precio, precio_usd, 
                                 imagen_url, imagen_mosaico_url, descripcion, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        """, (producto_data['nombre'], producto_data['categoria'], producto_data['subcategoria'],
              producto_data['precio'], producto_data['precio_usd'], 
              producto_data['imagen_url'], producto_data['imagen_mosaico_url'], 
              producto_data['descripcion']))
        
        producto_id = cursor.lastrowid
        print(f"✅ Producto creado: {producto_data['nombre']}")
        return producto_id, True

def main():
    try:
        # Conectar a la base de datos
        conn = conectar_db()
        print("🔗 Conectado a la base de datos")
        
        # Definir productos de revestimientos con sus datos
        productos_revestimientos = [
            {
                'nombre': 'Símil Piedra',
                'categoria': 'Revestimientos',
                'subcategoria': 'Simil Piedra',
                'precio': 45000,
                'precio_usd': 45,
                'imagen_url': 'img/products/simil_piedra_molde.jpg',
                'imagen_mosaico_url': 'img/products/simil_piedra_mosaico.html',
                'descripcion': '8 piezas por molde'
            },
            {
                'nombre': 'Murete Cuarcita',
                'categoria': 'Revestimientos',
                'subcategoria': 'Maderas',
                'precio': 42000,
                'precio_usd': 42,
                'imagen_url': 'img/products/murete_quarzita_molde.jpg',
                'imagen_mosaico_url': 'img/products/murete_quarzita_mosaico.png',
                'descripcion': '3 piezas por molde'
            },
            {
                'nombre': 'Quebracho',
                'categoria': 'Revestimientos',
                'subcategoria': 'Maderas',
                'precio': 42000,
                'precio_usd': 42,
                'imagen_url': 'img/products/quebracho_molde.jpg',
                'imagen_mosaico_url': 'img/products/quebracho_mosaico.png',
                'descripcion': '3 piezas por molde'
            },
            {
                'nombre': 'Corteza',
                'categoria': 'Revestimientos',
                'subcategoria': 'Maderas',
                'precio': 42000,
                'precio_usd': 42,
                'imagen_url': 'img/products/corteza_molde.jpg',
                'imagen_mosaico_url': 'img/products/corteza_mosaico.png',
                'descripcion': '3 piezas por molde'
            },
            {
                'nombre': 'Trapezoide',
                'categoria': 'Revestimientos',
                'subcategoria': 'Geometricos',
                'precio': 38000,
                'precio_usd': 38,
                'imagen_url': 'img/products/trapezoide_molde.jpg',
                'imagen_mosaico_url': 'img/products/trapezoidegris_mosaico.png',
                'descripcion': 'Molde geométrico para revestimientos'
            },
            {
                'nombre': 'Ondas',
                'categoria': 'Revestimientos',
                'subcategoria': 'Geometricos',
                'precio': 38000,
                'precio_usd': 38,
                'imagen_url': 'img/products/ondas_molde.jpg',
                'imagen_mosaico_url': 'img/products/ondasgris_mosaico.png',
                'descripcion': 'Molde con diseño de ondas'
            },
            {
                'nombre': 'Piedra Encastrable',
                'categoria': 'Revestimientos',
                'subcategoria': 'Encastrables',
                'precio': 44000,
                'precio_usd': 44,
                'imagen_url': 'img/products/piedra_encastrable_molde.jpg',
                'imagen_mosaico_url': 'img/products/piedra_encastrablegris_mosaico.png',
                'descripcion': 'Molde de piedra con sistema encastrable'
            },
            {
                'nombre': '3D',
                'categoria': 'Revestimientos',
                'subcategoria': 'Geometricos',
                'precio': 48000,
                'precio_usd': 48,
                'imagen_url': 'img/products/3d_molde.jpg',
                'imagen_mosaico_url': 'img/products/revestimiento_3dgris_mosaico.png',
                'descripcion': '3 piezas de 35x11,5cm'
            },
            {
                'nombre': 'Revestimiento 20x40',
                'categoria': 'Revestimientos',
                'subcategoria': 'Rectangulares',
                'precio': 40000,
                'precio_usd': 40,
                'imagen_url': 'img/products/revestimiento_20x40_molde.jpg',
                'imagen_mosaico_url': 'img/products/revestimiento_20x40_yeso_mosaico.html',
                'descripcion': '2 piezas por molde'
            },
            {
                'nombre': 'Laja 20x40',
                'categoria': 'Revestimientos',
                'subcategoria': 'Rectangulares',
                'precio': 40000,
                'precio_usd': 40,
                'imagen_url': 'img/products/laja_n2_40x20_molde.jpg',
                'imagen_mosaico_url': 'img/products/laja_20x40_yeso_mosaico.html',
                'descripcion': '2 piezas por molde'
            }
        ]
        
        productos_creados = 0
        productos_actualizados = 0
        
        for producto in productos_revestimientos:
            producto_id, es_nuevo = insertar_o_actualizar_producto(conn, producto)
            if es_nuevo:
                productos_creados += 1
            else:
                productos_actualizados += 1
        
        # Confirmar cambios
        conn.commit()
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN:")
        print(f"   • Productos nuevos creados: {productos_creados}")
        print(f"   • Productos actualizados: {productos_actualizados}")
        print(f"   • Total productos procesados: {len(productos_revestimientos)}")
        
        # Verificar productos activos en la categoría
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM productos 
            WHERE categoria = 'Revestimientos' AND activo = 1
        """)
        total_activos = cursor.fetchone()[0]
        print(f"   • Total productos activos en Revestimientos: {total_activos}")
        
        # Mostrar productos por subcategoría
        print(f"\n📋 PRODUCTOS POR SUBCATEGORÍA:")
        subcategorias = ['Simil Piedra', 'Maderas', 'Geometricos', 'Encastrables', 'Rectangulares']
        for subcategoria in subcategorias:
            cursor.execute("""
                SELECT COUNT(*) FROM productos 
                WHERE categoria = 'Revestimientos' AND subcategoria = ? AND activo = 1
            """, (subcategoria,))
            count = cursor.fetchone()[0]
            print(f"   • {subcategoria}: {count} productos")
        
        conn.close()
        print(f"\n✅ ¡Migración de revestimientos completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
