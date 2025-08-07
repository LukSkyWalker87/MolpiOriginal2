import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

print("Corrigiendo categorías de productos 50x50...")

# Actualizar la categoría de los productos nuevos (IDs 98-105)
cursor.execute("""
    UPDATE productos 
    SET categoria = 'Pisos y Zócalos' 
    WHERE id BETWEEN 98 AND 105 AND subcategoria = 'Línea 50x50'
""")

productos_actualizados = cursor.rowcount
conn.commit()

print(f"Se actualizaron {productos_actualizados} productos")

# Verificar que se actualizaron correctamente
cursor.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
productos = cursor.fetchall()

print(f"\nProductos en Línea 50x50 después de la corrección:")
for producto in productos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, Categoría: '{producto[2]}', Subcategoría: '{producto[3]}'")

print(f"\nTotal productos 50x50: {len(productos)}")

conn.close()
