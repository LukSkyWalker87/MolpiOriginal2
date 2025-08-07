import requests
import json

try:
    # Hacer petición a la API de productos
    response = requests.get('http://localhost:5000/productos')
    
    if response.status_code == 200:
        productos = response.json()
        
        # Buscar productos Vainilla
        vainilla_productos = [p for p in productos if 'Vainilla' in p.get('nombre', '')]
        
        print("Productos Vainilla desde la API:")
        for producto in vainilla_productos:
            print(f"ID: {producto.get('id')}")
            print(f"Nombre: {producto.get('nombre')}")
            print(f"Imagen molde: {producto.get('imagen_url')}")
            print(f"Imagen mosaico: {producto.get('imagen_mosaico_url')}")
            print(f"Todas las claves: {list(producto.keys())}")
            print("-" * 50)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error conectando con la API: {e}")
