#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def verificar_imagenes_mosaico_50x50():
    """
    Verifica qué imágenes de mosaico existen para los productos 50x50
    """
    
    db_path = "molpi.db"
    img_dir = "../www.molpi.com.ar/img/products/"
    
    print("=== VERIFICACIÓN DE IMÁGENES DE MOSAICO PARA LÍNEA 50x50 ===\n")
    
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
        
        for id_prod, nombre, imagen_molde in productos:
            print(f"📦 {nombre} (ID: {id_prod})")
            print(f"   Molde: {imagen_molde}")
            
            # Generar la URL del mosaico basándose en el molde
            imagen_mosaico = imagen_molde.replace('_molde.jpg', '_mosaico.png')
            print(f"   Mosaico esperado: {imagen_mosaico}")
            
            # Verificar si existe el archivo de mosaico
            ruta_mosaico = os.path.join(img_dir, imagen_mosaico.replace('img/products/', ''))
            
            if os.path.exists(ruta_mosaico):
                print(f"   ✅ Mosaico EXISTE")
            else:
                print(f"   ❌ Mosaico NO EXISTE")
                
                # Buscar archivos similares
                nombre_base = imagen_molde.replace('img/products/', '').replace('_molde.jpg', '')
                archivos_en_directorio = os.listdir(img_dir)
                posibles_mosaicos = [f for f in archivos_en_directorio if nombre_base in f and 'mosaico' in f]
                
                if posibles_mosaicos:
                    print(f"   🔍 Posibles alternativas encontradas:")
                    for archivo in posibles_mosaicos:
                        print(f"      - img/products/{archivo}")
                else:
                    print(f"   🔍 No se encontraron alternativas")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    verificar_imagenes_mosaico_50x50()
