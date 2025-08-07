import requests
import json

response = requests.get('http://127.0.0.1:5000/productos')
productos = response.json()

green_products = [p for p in productos if p['categoria'] == 'Green' and p['activo'] == 1]

print('Productos Green encontrados:')
for p in green_products:
    print(f'- ID: {p["id"]}, Nombre: "{p["nombre"]}"')

print(f'\nTotal productos Green activos: {len(green_products)}')
