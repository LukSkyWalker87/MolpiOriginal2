import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Buscar producto Laja Española
cursor.execute("SELECT id, nombre, imagen_url, subcategoria FROM productos WHERE nombre LIKE '%Laja%'")
results = cursor.fetchall()

print("Productos que contienen 'Laja':")
for row in results:
    print(f"ID: {row[0]}, Nombre: {row[1]}, URL: {row[2]}, Subcategoría: {row[3]}")

conn.close()
