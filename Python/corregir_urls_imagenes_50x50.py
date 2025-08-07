#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def corregir_urls_imagenes_50x50():
    """
    Corrige las URLs de las imágenes para productos específicos de la línea 50x50
    """
    
    # Conexión a la base de datos
    db_path = "molpi.db"
    
    # Mapeo de nombres de productos con sus URLs correctas
    correcciones = {
        "Adoquín Colonial": "img/products/laja_colonial_molde.jpg",
        "Deck Símil Madera": "img/products/deck_simil_madera_molde.jpg", 
        "Madera 50x25x6 / 2 piezas por molde": "img/products/madera_6_cm_molde.jpg",
        "Quebracho": "img/products/quebracho_molde.jpg",
        "Corteza": "img/products/corteza_molde.jpg"  # Para el ID 105, no el 35
    }
    
    print("=== CORRIGIENDO URLs DE IMÁGENES PARA PRODUCTOS 50x50 ===\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Primero mostrar los productos actuales
        print("📋 PRODUCTOS ANTES DE LA CORRECCIÓN:")
        cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
        productos_antes = cursor.fetchall()
        
        for producto in productos_antes:
            id_prod, nombre, imagen_actual = producto
            print(f"ID: {id_prod:3d} | Nombre: {nombre:35s} | Imagen: {imagen_actual}")
        
        print("\n" + "="*80 + "\n")
        
        # Realizar las correcciones
        productos_actualizados = 0
        
        for nombre_producto, nueva_url in correcciones.items():
            # Buscar el producto por nombre en la línea 50x50
            cursor.execute("""
                SELECT id, nombre, imagen_url 
                FROM productos 
                WHERE nombre = ? AND subcategoria = 'Línea 50x50'
            """, (nombre_producto,))
            
            resultado = cursor.fetchone()
            
            if resultado:
                id_prod, nombre, imagen_actual = resultado
                
                # Actualizar la URL de la imagen
                cursor.execute("""
                    UPDATE productos 
                    SET imagen_url = ? 
                    WHERE id = ?
                """, (nueva_url, id_prod))
                
                print(f"✅ ACTUALIZADO ID {id_prod}: {nombre}")
                print(f"   Antes: {imagen_actual}")
                print(f"   Ahora: {nueva_url}\n")
                
                productos_actualizados += 1
                
            else:
                print(f"❌ NO ENCONTRADO: {nombre_producto}\n")
        
        # Confirmar cambios
        conn.commit()
        
        print("="*80)
        print(f"✅ CORRECCIÓN COMPLETADA: {productos_actualizados} productos actualizados")
        print("="*80 + "\n")
        
        # Mostrar los productos después de la corrección
        print("📋 PRODUCTOS DESPUÉS DE LA CORRECCIÓN:")
        cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
        productos_despues = cursor.fetchall()
        
        for producto in productos_despues:
            id_prod, nombre, imagen_url = producto
            print(f"ID: {id_prod:3d} | Nombre: {nombre:35s} | Imagen: {imagen_url}")
        
        conn.close()
        
        print(f"\n🎉 ¡PROCESO COMPLETADO! {productos_actualizados} URLs corregidas exitosamente.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    corregir_urls_imagenes_50x50()
