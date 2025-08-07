import sqlite3

conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

cursor.execute('SELECT id, nombre, imagen_url, imagen_mosaico_url FROM productos WHERE linea = "50x50" ORDER BY id')
productos = cursor.fetchall()

print(f'Productos 50x50 encontrados: {len(productos)}')
print('\nLista de productos:')
for p in productos:
    print(f'ID: {p[0]} - Nombre: {p[1]} - Mosaico: {p[3] if p[3] else "Sin mosaico"}')

conn.close()
