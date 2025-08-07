import json
from urllib.request import urlopen

try:
    # Probar la API
    with urlopen('http://localhost:5000/productos') as response:
        data = json.loads(response.read().decode())
    
    # Filtrar productos Vainilla
    vainilla_products = [p for p in data if 'Vainilla' in p.get('nombre', '')]
    
    print("=== PRODUCTOS VAINILLA DESDE LA API ===")
    for producto in vainilla_products:
        print(f"ID: {producto.get('id')}")
        print(f"Nombre: {producto.get('nombre')}")
        print(f"Imagen molde: {producto.get('imagen_url')}")
        print(f"Imagen mosaico: {producto.get('imagen_mosaico_url')}")
        print(f"Claves disponibles: {sorted(producto.keys())}")
        print("-" * 60)
        
except Exception as e:
    print(f"Error: {e}")
