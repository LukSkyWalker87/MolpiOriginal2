import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Mostrar los productos con los IDs problemáticos
ids = [160, 161, 158, 159]
c.execute(f"SELECT * FROM productos WHERE id IN ({','.join(['?']*len(ids))})", ids)
rows = c.fetchall()
print('Productos encontrados:', rows)

conn.close()
