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
        
        # Definir productos de insumos con sus datos
        productos_insumos = [
            # Curadores
            {
                'nombre': 'Curador Color Negro',
                'categoria': 'Insumos',
                'subcategoria': 'Curadores',
                'precio': 8500,
                'precio_usd': 8.5,
                'imagen_url': 'img/products/insumos/insumos_bidon_negro.jpg',
                'imagen_mosaico_url': 'img/products/insumos/insumos_botella_negro.png',
                'descripcion': 'Curador para cemento color negro - Bidón 5L o Botella 1L'
            },
            {
                'nombre': 'Curador Color Natural',
                'categoria': 'Insumos',
                'subcategoria': 'Curadores',
                'precio': 8000,
                'precio_usd': 8,
                'imagen_url': 'img/products/insumos/insumos_bidon_natural.jpg',
                'imagen_mosaico_url': 'img/products/insumos/insumos_botella_natural.png',
                'descripcion': 'Curador para cemento color natural - Bidón 5L o Botella 1L'
            },
            {
                'nombre': 'Curador Color Rojo',
                'categoria': 'Insumos',
                'subcategoria': 'Curadores',
                'precio': 9000,
                'precio_usd': 9,
                'imagen_url': 'img/products/insumos/insumos_bidon_rojo.jpg',
                'imagen_mosaico_url': 'img/products/insumos/insumos_botella_rojo.png',
                'descripcion': 'Curador para cemento color rojo - Bidón 5L o Botella 1L'
            },
            {
                'nombre': 'Curador Color Terracota',
                'categoria': 'Insumos',
                'subcategoria': 'Curadores',
                'precio': 9000,
                'precio_usd': 9,
                'imagen_url': 'img/products/insumos/insumos_bidon_terracota.jpg',
                'imagen_mosaico_url': 'img/products/insumos/insumos_botella_terracota.png',
                'descripcion': 'Curador para cemento color terracota - Bidón 5L o Botella 1L'
            },
            
            # Pigmentos Básicos
            {
                'nombre': 'Pigmento en Polvo Rojo',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Básicos',
                'precio': 3500,
                'precio_usd': 3.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_rojo.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento en polvo de óxido de hierro color rojo'
            },
            {
                'nombre': 'Pigmento en Polvo Amarillo',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Básicos',
                'precio': 3500,
                'precio_usd': 3.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_amarillo.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento en polvo de óxido de hierro color amarillo'
            },
            {
                'nombre': 'Pigmento en Polvo Negro',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Básicos',
                'precio': 3500,
                'precio_usd': 3.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_negro.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento en polvo de óxido de hierro color negro'
            },
            {
                'nombre': 'Pigmento en Polvo Gris',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Básicos',
                'precio': 3500,
                'precio_usd': 3.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_gris.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento en polvo de óxido de hierro color gris'
            },
            {
                'nombre': 'Pigmento en Polvo Terracota',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Básicos',
                'precio': 3800,
                'precio_usd': 3.8,
                'imagen_url': 'img/products/insumos/insumos_pigmento_terracota.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento en polvo de óxido de hierro color terracota'
            },
            
            # Pigmentos Concentrados
            {
                'nombre': 'Pigmento en Polvo Verde Concentrado',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Concentrados',
                'precio': 4500,
                'precio_usd': 4.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_verde_concentrado.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento concentrado en polvo de óxido de hierro color verde'
            },
            {
                'nombre': 'Pigmento en Polvo Azul Concentrado',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Concentrados',
                'precio': 4500,
                'precio_usd': 4.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_azul_concentrado.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento concentrado en polvo de óxido de hierro color azul'
            },
            {
                'nombre': 'Pigmento en Polvo Habano Concentrado',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Concentrados',
                'precio': 4500,
                'precio_usd': 4.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_habano_concentrado.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento concentrado en polvo de óxido de hierro color habano'
            },
            {
                'nombre': 'Pigmento en Polvo Marrón Concentrado',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Concentrados',
                'precio': 4500,
                'precio_usd': 4.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_marron_concentrado.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento concentrado en polvo de óxido de hierro color marrón'
            },
            {
                'nombre': 'Pigmento en Polvo Siena Concentrado',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Concentrados',
                'precio': 4500,
                'precio_usd': 4.5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_siena_concentrado.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento concentrado en polvo de óxido de hierro color siena'
            },
            
            # Pigmentos Extra
            {
                'nombre': 'Pigmento en Polvo Verde Extra',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Extra',
                'precio': 5000,
                'precio_usd': 5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_verde_extra.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento extra en polvo de óxido de hierro color verde'
            },
            {
                'nombre': 'Pigmento en Polvo Azul Extra',
                'categoria': 'Insumos',
                'subcategoria': 'Pigmentos Extra',
                'precio': 5000,
                'precio_usd': 5,
                'imagen_url': 'img/products/insumos/insumos_pigmento_azul_extra.jpg',
                'imagen_mosaico_url': None,
                'descripcion': 'Pigmento extra en polvo de óxido de hierro color azul'
            }
        ]
        
        productos_creados = 0
        productos_actualizados = 0
        
        for producto in productos_insumos:
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
        print(f"   • Total productos procesados: {len(productos_insumos)}")
        
        # Verificar productos activos en la categoría
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM productos 
            WHERE categoria = 'Insumos' AND activo = 1
        """)
        total_activos = cursor.fetchone()[0]
        print(f"   • Total productos activos en Insumos: {total_activos}")
        
        # Mostrar productos por subcategoría
        print(f"\n📋 PRODUCTOS POR SUBCATEGORÍA:")
        subcategorias = ['Curadores', 'Pigmentos Básicos', 'Pigmentos Concentrados', 'Pigmentos Extra']
        for subcategoria in subcategorias:
            cursor.execute("""
                SELECT COUNT(*) FROM productos 
                WHERE categoria = 'Insumos' AND subcategoria = ? AND activo = 1
            """, (subcategoria,))
            count = cursor.fetchone()[0]
            if count > 0:
                print(f"   • {subcategoria}: {count} productos")
        
        conn.close()
        print(f"\n✅ ¡Migración de insumos completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
