import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Verificar todos los productos de línea 50x50
cursor.execute("SELECT id, nombre, subcategoria, activo FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
productos = cursor.fetchall()

print("Productos en Línea 50x50:")
for producto in productos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Subcategoría: {producto[2]}, Activo: {producto[3]}")

print(f"\nTotal productos 50x50: {len(productos)}")

# También verificar si hay productos con subcategorías similares
cursor.execute("SELECT DISTINCT subcategoria FROM productos WHERE subcategoria LIKE '%50%'")
subcategorias = cursor.fetchall()

print(f"\nSubcategorías que contienen '50':")
for sub in subcategorias:
    print(f"- {sub[0]}")

conn.close()
