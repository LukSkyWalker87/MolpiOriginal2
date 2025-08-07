import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()
c.execute("SELECT id, nombre FROM productos WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20'")
rows = c.fetchall()
print("Productos encontrados:")
for row in rows:
    print(f"ID: {row[0]}, Nombre: {row[1]}")
conn.close()
