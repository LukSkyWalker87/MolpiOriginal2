#!/usr/bin/env python3
import requests
import json

def crear_producto_podotactil(producto_data):
    url = "http://127.0.0.1:5000/productos"
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, headers=headers, json=producto_data)
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Producto '{producto_data['nombre']}' creado con ID: {result['id']}")
        return True
    else:
        print(f"❌ Error creando '{producto_data['nombre']}': {response.status_code} - {response.text}")
        return False

# Productos podotáctiles a crear (solo recrear el que se borró)
productos_podotactiles = [
    {
        'nombre': 'Pisos Podotáctiles con Círculos',
        'categoria': 'Podotáctiles',
        'subcategoria': 'Discapacidad',
        'descripcion': 'Los pisos podotáctiles de advertencia funcionan para todos, nos advierten a todos de que hay peligro inminente en nuestro camino, y sobre todo les ayuda a personas ciegas a saber que no deben avanzar; son conocidos también como señal de Stop.',
        'imagen_url': 'img/products/circulos_ciegos_molde.jpg',
        'imagen_mosaico_url': 'img/products/circulos_ciegos_mosaico.png',
        'precio': 0,
        'precio_usd': 0,
        'pdf_url': ''
    }
]

print("🚀 Creando productos podotáctiles...")

for producto in productos_podotactiles:
    crear_producto_podotactil(producto)

print("\n✅ Proceso completado!")
