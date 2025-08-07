import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Buscar productos Vainilla
c.execute('SELECT id, nombre, imagen_url, imagen_mosaico_url FROM productos WHERE nombre LIKE "%Vainilla%"')
productos = c.fetchall()

print("Productos Vainilla encontrados:")
for producto in productos:
    print(f"ID: {producto[0]}")
    print(f"Nombre: {producto[1]}")
    print(f"Imagen molde: {producto[2]}")
    print(f"Imagen mosaico: {producto[3]}")
    print("-" * 50)

conn.close()
