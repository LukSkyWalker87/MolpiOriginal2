import requests
import json

response = requests.get('http://127.0.0.1:5000/productos/linea/50x50')
productos = response.json()

print(f'Productos 50x50 desde API: {len(productos)}')
print('\nLista de productos:')
for p in productos:
    mosaico = p.get('imagen_mosaico_url', 'Sin mosaico')
    print(f'ID: {p["id"]} - {p["nombre"]} - Mosaico: {mosaico}')
