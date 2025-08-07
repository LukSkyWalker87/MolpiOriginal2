#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def actualizar_imagenes_green():
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar', 'instance', 'molpi.db')
    
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en {db_path}")
        return
    
    print(f"📁 Usando base de datos: {db_path}")
    
    # Mapeo de imágenes de mosaico para productos existentes
    actualizaciones = [
        {
            'nombre': 'Rombo Green',
            'imagen_mosaico_url': 'img/products/rombo_green_mosaico.png'
        },
        {
            'nombre': 'Recto Green',
            'imagen_mosaico_url': 'img/products/recto_green_mosaico.png'
        },
        {
            'nombre': 'Círculos Green',
            'imagen_mosaico_url': 'img/products/circulos_green_mosaico.png'
        }
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🟢 Actualizando imágenes de mosaico para productos Green...")
    
    for actualizar in actualizaciones:
        try:
            # Actualizar la imagen de mosaico
            cursor.execute("""
                UPDATE productos 
                SET imagen_mosaico_url = ?
                WHERE nombre = ? AND categoria = 'Green'
            """, (actualizar['imagen_mosaico_url'], actualizar['nombre']))
            
            if cursor.rowcount > 0:
                print(f"✅ Actualizado '{actualizar['nombre']}' con imagen mosaico: {actualizar['imagen_mosaico_url']}")
            else:
                print(f"⚠️  No se encontró el producto '{actualizar['nombre']}'")
            
        except Exception as e:
            print(f"❌ Error al actualizar '{actualizar['nombre']}': {e}")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Actualización completada!")
    
    # Verificar las actualizaciones
    print("\n📋 Verificando productos Green actualizados...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, nombre, imagen_url, imagen_mosaico_url
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY id
    """)
    
    productos = cursor.fetchall()
    
    for producto in productos:
        id_prod, nombre, imagen_url, imagen_mosaico_url = producto
        print(f"🆔 {id_prod}: {nombre}")
        print(f"   🖼️  Molde: {imagen_url}")
        print(f"   🎨 Mosaico: {imagen_mosaico_url}")
    
    conn.close()

if __name__ == "__main__":
    actualizar_imagenes_green()
