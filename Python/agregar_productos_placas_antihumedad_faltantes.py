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
        
        # Definir productos de placas antihumedad con sus datos
        productos_placas_antihumedad = [
            {
                'nombre': 'Trapezoide Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Geometricos',
                'precio': 40000,
                'precio_usd': 40,
                'imagen_url': 'img/products/trapezoide_molde.jpg',
                'imagen_mosaico_url': 'img/products/trapezoide_mosaico.png',
                'descripcion': 'Molde trapezoide para placas antihumedad'
            },
            {
                'nombre': 'Ondas Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Geometricos',
                'precio': 40000,
                'precio_usd': 40,
                'imagen_url': 'img/products/ondas_molde.jpg',
                'imagen_mosaico_url': 'img/products/ondas_mosaico.png',
                'descripcion': 'Molde con diseño de ondas para placas antihumedad'
            },
            {
                'nombre': 'Piedra Encastrable Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Encastrables',
                'precio': 46000,
                'precio_usd': 46,
                'imagen_url': 'img/products/piedra_encastrable_molde.jpg',
                'imagen_mosaico_url': 'img/products/piedra_encastrable_mosaico.png',
                'descripcion': 'Molde de piedra encastrable para placas antihumedad'
            },
            {
                'nombre': '3D Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Tridimensionales',
                'precio': 50000,
                'precio_usd': 50,
                'imagen_url': 'img/products/3d_molde.jpg',
                'imagen_mosaico_url': 'img/products/revestimiento_3d_mosaico.png',
                'descripcion': '3 piezas de 35x11,5cm para placas antihumedad'
            },
            {
                'nombre': 'Revestimiento 20x40 Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Rectangulares',
                'precio': 42000,
                'precio_usd': 42,
                'imagen_url': 'img/products/revestimiento_20x40_molde.jpg',
                'imagen_mosaico_url': 'img/products/revestimiento_20x40_yeso_mosaico.html',
                'descripcion': 'Molde rectangular 20x40 para placas antihumedad'
            },
            {
                'nombre': 'Laja 20x40 Antihumedad',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Rectangulares',
                'precio': 42000,
                'precio_usd': 42,
                'imagen_url': 'img/products/laja_n2_40x20_molde.jpg',
                'imagen_mosaico_url': 'img/products/laja_20x40_yeso_mosaico.html',
                'descripcion': 'Molde laja 20x40 para placas antihumedad'
            },
            {
                'nombre': 'Travertino Viejo',
                'categoria': 'Placas Antihumedad',
                'subcategoria': 'Texturas',
                'precio': 44000,
                'precio_usd': 44,
                'imagen_url': 'img/products/travertino_viejo_molde.jpg',
                'imagen_mosaico_url': 'img/products/travertino_viejo_yeso_mosaico.png',
                'descripcion': 'Molde con textura travertino viejo para placas antihumedad'
            }
        ]
        
        productos_creados = 0
        productos_actualizados = 0
        
        for producto in productos_placas_antihumedad:
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
        print(f"   • Total productos procesados: {len(productos_placas_antihumedad)}")
        
        # Verificar productos activos en la categoría
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM productos 
            WHERE categoria = 'Placas Antihumedad' AND activo = 1
        """)
        total_activos = cursor.fetchone()[0]
        print(f"   • Total productos activos en Placas Antihumedad: {total_activos}")
        
        # Mostrar productos por subcategoría
        print(f"\n📋 PRODUCTOS POR SUBCATEGORÍA:")
        subcategorias = ['Geometricos', 'Encastrables', 'Tridimensionales', 'Rectangulares', 'Texturas']
        for subcategoria in subcategorias:
            cursor.execute("""
                SELECT COUNT(*) FROM productos 
                WHERE categoria = 'Placas Antihumedad' AND subcategoria = ? AND activo = 1
            """, (subcategoria,))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"   • {subcategoria}: {count} productos")
        
        conn.close()
        print(f"\n✅ ¡Migración de placas antihumedad completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
