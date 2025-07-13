import requests

r = requests.get('http://localhost:5000/productos')
datos = r.json()

print('Total productos únicos:', len(set(p['id'] for p in datos)))
print('Primer producto:')
p = datos[0]
print(f'ID: {p["id"]}')
print(f'Nombre: {p["nombre"]}')
print(f'Imagen: {p["imagen_url"]}')
print(f'Categoría: {p["categoria"]}')
print(f'Subcategoría: {p["subcategoria"]}')
