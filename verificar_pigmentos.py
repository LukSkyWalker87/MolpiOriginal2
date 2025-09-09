import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'python', 'molpi.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Mostrar todas las subcategorías 'Pigmentos' y su categoria_id
c.execute("SELECT id, nombre, categoria_id FROM subcategorias WHERE nombre = 'Pigmentos'")
rows = c.fetchall()
print(rows)
conn.close()
