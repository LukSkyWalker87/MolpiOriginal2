import sqlite3

conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Verificar estructura de la tabla
cursor.execute("PRAGMA table_info(productos)")
columnas = cursor.fetchall()
print("Columnas de la tabla productos:")
for col in columnas:
    print(f"  {col[1]} ({col[2]})")

# Buscar productos que contengan "50x50" en el nombre
cursor.execute('SELECT id, nombre, imagen_url, imagen_mosaico_url FROM productos WHERE nombre LIKE "%50x50%" ORDER BY id')
productos = cursor.fetchall()

print(f'\nProductos con "50x50" en el nombre: {len(productos)}')
print('\nLista de productos:')
for p in productos:
    print(f'ID: {p[0]} - Nombre: {p[1]} - Mosaico: {p[3] if p[3] else "Sin mosaico"}')

conn.close()
