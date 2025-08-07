#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def verificar_imagenes_50x50():
    # Conectar a la base de datos
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    print("=== VERIFICACIÓN DE IMÁGENES PARA PRODUCTOS 50x50 ===\n")
    
    # Buscar productos de la línea 50x50
    cursor.execute("""
        SELECT id, nombre, imagen_url, descripcion 
        FROM productos 
        WHERE subcategoria = 'Línea 50x50' 
        ORDER BY id
    """)
    
    productos = cursor.fetchall()
    print(f"Total productos en Línea 50x50: {len(productos)}\n")
    
    # Productos específicos mencionados por el usuario
    productos_problema = [
        "Adoquín Colonial",
        "Deck Antideslizante", 
        "Deck Símil Madera",
        "Liso",
        "Madera 50x25x6 / 2 piezas por molde"
    ]
    
    print("=== PRODUCTOS MENCIONADOS CON PROBLEMAS DE IMAGEN ===")
    for nombre_problema in productos_problema:
        print(f"\nBuscando: {nombre_problema}")
        encontrado = False
        for producto in productos:
            if nombre_problema.lower() in producto[1].lower():
                print(f"  ✓ ID: {producto[0]}")
                print(f"  ✓ Nombre: {producto[1]}")
                print(f"  ✓ Imagen: {producto[2]}")
                print(f"  ✓ Descripción: {producto[3]}")
                
                # Verificar si existe el archivo de imagen
                if producto[2]:
                    ruta_imagen = f"../www.molpi.com.ar/{producto[2]}"
                    if os.path.exists(ruta_imagen):
                        print(f"  ✓ Archivo de imagen existe: {ruta_imagen}")
                    else:
                        print(f"  ❌ Archivo de imagen NO existe: {ruta_imagen}")
                else:
                    print(f"  ❌ No tiene ruta de imagen definida")
                encontrado = True
                break
        
        if not encontrado:
            print(f"  ❌ Producto no encontrado en la base de datos")
    
    print("\n=== TODOS LOS PRODUCTOS 50x50 ===")
    for producto in productos:
        print(f"ID: {producto[0]:<3} | Nombre: {producto[1]:<35} | Imagen: {producto[2] or 'SIN IMAGEN'}")
    
    conn.close()

if __name__ == "__main__":
    verificar_imagenes_50x50()
