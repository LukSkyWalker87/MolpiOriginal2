import requests
import json

# Probar el endpoint de categorías
base_url = "http://127.0.0.1:5000"

print("=== PROBANDO ENDPOINT DE CATEGORÍAS ===")

# 1. Obtener todas las categorías
print("\n1. Todas las categorías:")
response = requests.get(f"{base_url}/categorias")
categorias = response.json()
print(f"Total categorías: {len(categorias)}")

for categoria in categorias:
    print(f"  - ID: {categoria['id']}, Nombre: '{categoria['nombre']}', Activo: {categoria['activo']}")

# 2. Comparar con las categorías de los productos
print("\n2. Categorías de productos vs categorías de la tabla:")
response = requests.get(f"{base_url}/productos")
productos = response.json()

categorias_productos = set()
for producto in productos:
    categorias_productos.add(producto['categoria'])

categorias_tabla = set()
for categoria in categorias:
    categorias_tabla.add(categoria['nombre'])

print(f"Categorías en productos: {sorted(categorias_productos)}")
print(f"Categorías en tabla: {sorted(categorias_tabla)}")

# 3. Verificar diferencias
print("\n3. Diferencias:")
print(f"En productos pero no en tabla: {categorias_productos - categorias_tabla}")
print(f"En tabla pero no en productos: {categorias_tabla - categorias_productos}")
