import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Verificar categorías de los productos 50x50
cursor.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
productos = cursor.fetchall()

print("Productos en Línea 50x50 con sus categorías:")
for producto in productos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Categoría: '{producto[2]}', Subcategoría: '{producto[3]}'")

print(f"\nTotal productos: {len(productos)}")

# Verificar si hay productos sin categoría o con categoría diferente
cursor.execute("SELECT id, nombre, categoria FROM productos WHERE id BETWEEN 98 AND 105")
productos_nuevos = cursor.fetchall()

print(f"\nProductos nuevos (IDs 98-105):")
for producto in productos_nuevos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Categoría: '{producto[2]}'")

conn.close()
