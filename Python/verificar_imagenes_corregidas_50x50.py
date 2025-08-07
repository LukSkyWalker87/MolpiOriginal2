#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

def verificar_imagenes_corregidas_50x50():
    """
    Verifica que todas las imágenes de productos 50x50 existan después de las correcciones
    """
    
    # Directorio base de imágenes
    img_dir = "../www.molpi.com.ar/img/products/"
    db_path = "molpi.db"
    
    print("=== VERIFICACIÓN DE IMÁGENES DESPUÉS DE CORRECCIONES ===\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todos los productos de la línea 50x50
        cursor.execute("""
            SELECT id, nombre, imagen_url 
            FROM productos 
            WHERE subcategoria = 'Línea 50x50' 
            ORDER BY id
        """)
        
        productos = cursor.fetchall()
        
        imagenes_faltantes = []
        imagenes_existentes = []
        
        for id_prod, nombre, imagen_url in productos:
            ruta_completa = os.path.join(img_dir, imagen_url.replace('img/products/', ''))
            
            if os.path.exists(ruta_completa):
                imagenes_existentes.append((id_prod, nombre, imagen_url))
                print(f"✅ ID {id_prod:3d}: {nombre:35s} | {imagen_url}")
            else:
                imagenes_faltantes.append((id_prod, nombre, imagen_url))
                print(f"❌ ID {id_prod:3d}: {nombre:35s} | {imagen_url} - NO EXISTE")
        
        print(f"\n📊 RESUMEN:")
        print(f"   ✅ Imágenes existentes: {len(imagenes_existentes)}")
        print(f"   ❌ Imágenes faltantes: {len(imagenes_faltantes)}")
        
        if imagenes_faltantes:
            print(f"\n🔧 IMÁGENES QUE NECESITAN SER CREADAS:")
            for id_prod, nombre, imagen_url in imagenes_faltantes:
                print(f"   - {imagen_url}")
        else:
            print(f"\n🎉 ¡TODAS LAS IMÁGENES EXISTEN CORRECTAMENTE!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    verificar_imagenes_corregidas_50x50()
