#!/usr/bin/env python3
import requests
import json

def verificar_producto(producto_id):
    url = f"http://127.0.0.1:5000/productos?incluir_inactivos=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        productos = response.json()
        producto = next((p for p in productos if p['id'] == producto_id), None)
        
        if producto:
            print(f"🔍 Producto ID {producto_id}:")
            print(f"   Nombre: {producto['nombre']}")
            print(f"   Activo: {producto['activo']}")
            print(f"   Categoría: {producto['categoria']}")
            return producto
        else:
            print(f"❌ Producto ID {producto_id} no encontrado")
            return None
    else:
        print(f"❌ Error al consultar productos: {response.status_code}")
        return None

# Verificar todos los productos podotáctiles
print("🔍 Verificando estado de productos podotáctiles...")
print()

for producto_id in [108, 110, 113]:
    verificar_producto(producto_id)
    print()
