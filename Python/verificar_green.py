#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def verificar_productos_green():
    # Ruta a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar', 'instance', 'molpi.db')
    
    if not os.path.exists(db_path):
        db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en {db_path}")
        return
    
    print(f"📁 Usando base de datos: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🟢 === VERIFICACIÓN DE PRODUCTOS GREEN ===")
    
    # Obtener todos los productos Green
    cursor.execute("""
        SELECT id, nombre, categoria, subcategoria, imagen_url, imagen_mosaico_url, activo
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY id
    """)
    
    productos = cursor.fetchall()
    
    if not productos:
        print("❌ No se encontraron productos Green")
        return
    
    print(f"\n📦 Total productos Green: {len(productos)}")
    
    activos = 0
    inactivos = 0
    
    for producto in productos:
        id_prod, nombre, categoria, subcategoria, imagen_url, imagen_mosaico_url, activo = producto
        
        estado = "✅ Activo" if activo == 1 else "❌ Inactivo"
        if activo == 1:
            activos += 1
        else:
            inactivos += 1
        
        print(f"\n🆔 ID: {id_prod}")
        print(f"📛 Nombre: {nombre}")
        print(f"📂 Categoría: {categoria}")
        print(f"📁 Subcategoría: {subcategoria}")
        print(f"🖼️  Imagen molde: {imagen_url}")
        print(f"🎨 Imagen mosaico: {imagen_mosaico_url}")
        print(f"🔄 Estado: {estado}")
        
        # Verificar si las imágenes existen
        base_path = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar')
        
        if imagen_url:
            img_path = os.path.join(base_path, imagen_url)
            if os.path.exists(img_path):
                print(f"   ✅ Imagen molde existe")
            else:
                print(f"   ❌ Imagen molde NO existe: {img_path}")
        
        if imagen_mosaico_url:
            mos_path = os.path.join(base_path, imagen_mosaico_url)
            if os.path.exists(mos_path):
                print(f"   ✅ Imagen mosaico existe")
            else:
                print(f"   ❌ Imagen mosaico NO existe: {mos_path}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   🟢 Productos activos: {activos}")
    print(f"   🔴 Productos inactivos: {inactivos}")
    print(f"   📦 Total productos: {len(productos)}")
    
    # Verificar API response
    print(f"\n🌐 Verificando respuesta de API...")
    import requests
    try:
        response = requests.get('http://127.0.0.1:5000/productos')
        if response.status_code == 200:
            productos_api = response.json()
            productos_green_api = [p for p in productos_api if p.get('categoria') == 'Green' and p.get('activo') == 1]
            print(f"   ✅ API responde correctamente")
            print(f"   🟢 Productos Green activos en API: {len(productos_green_api)}")
            
            for producto in productos_green_api:
                print(f"      - {producto.get('nombre')} (ID: {producto.get('id')})")
        else:
            print(f"   ❌ API error: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Error conectando a API: {e}")
    
    conn.close()
    print("\n✅ Verificación completada!")

if __name__ == "__main__":
    verificar_productos_green()
