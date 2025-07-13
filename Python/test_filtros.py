import requests
import json

# Probar el endpoint de productos con filtros
base_url = "http://127.0.0.1:5000"

print("=== PROBANDO ENDPOINTS DE PRODUCTOS ===")

# 1. Obtener todos los productos
print("\n1. Todos los productos:")
response = requests.get(f"{base_url}/productos")
todos_productos = response.json()
print(f"Total productos: {len(todos_productos)}")

# 2. Filtrar por categoría "Pisos y Zócalos"
print("\n2. Productos de 'Pisos y Zócalos':")
response = requests.get(f"{base_url}/productos?categoria=Pisos y Zócalos")
productos_pisos = response.json()
print(f"Total productos de Pisos y Zócalos: {len(productos_pisos)}")

# Mostrar algunos productos de ejemplo
for i, producto in enumerate(productos_pisos[:5]):
    print(f"  {i+1}. {producto['nombre']} - Categoría: {producto['categoria']} - Subcategoría: {producto['subcategoria']}")

# 3. Filtrar por categoría "Insumos"
print("\n3. Productos de 'Insumos':")
response = requests.get(f"{base_url}/productos?categoria=Insumos")
productos_insumos = response.json()
print(f"Total productos de Insumos: {len(productos_insumos)}")

# Mostrar algunos productos de ejemplo
for i, producto in enumerate(productos_insumos[:5]):
    print(f"  {i+1}. {producto['nombre']} - Categoría: {producto['categoria']} - Subcategoría: {producto['subcategoria']}")

# 4. Verificar si hay productos mixtos
print("\n4. Verificando categorías en la respuesta de 'Pisos y Zócalos':")
categorias_encontradas = set()
for producto in productos_pisos:
    categorias_encontradas.add(producto['categoria'])

print(f"Categorías encontradas: {categorias_encontradas}")

# 5. Probar con URL encode
print("\n5. Probando con URL encode:")
import urllib.parse
categoria_encoded = urllib.parse.quote("Pisos y Zócalos")
response = requests.get(f"{base_url}/productos?categoria={categoria_encoded}")
productos_encoded = response.json()
print(f"Total productos con URL encode: {len(productos_encoded)}")
