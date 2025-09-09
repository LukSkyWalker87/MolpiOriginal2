import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'python', 'molpi.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Mostrar todas las subcategorías de Insumos
c.execute("SELECT id FROM categorias WHERE nombre = 'Insumos'")
row = c.fetchone()
if not row:
    print("No existe la categoría 'Insumos'")
    conn.close()
    exit(1)
categoria_id = row[0]

c.execute("SELECT id, nombre FROM subcategorias WHERE categoria_id = ?", (categoria_id,))
rows = c.fetchall()
print(rows)
conn.close()
