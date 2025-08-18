import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')

ids_a_borrar = [160, 161, 158, 159]

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Borrado físico definitivo de los productos
c.execute(f"DELETE FROM productos WHERE id IN ({','.join(['?']*len(ids_a_borrar))})", ids_a_borrar)
conn.commit()
print(f"Registros eliminados: {ids_a_borrar}")

conn.close()
