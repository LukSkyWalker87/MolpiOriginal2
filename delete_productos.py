import sqlite3
import os

# Ruta absoluta a la base de datos (ajusta si es necesario)
db_path = os.path.join(os.path.dirname(__file__), 'backend', 'molpi.db')

# IDs a eliminar
target_ids = [160, 161, 158, 159]

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Eliminación física (borrado total)
c.execute(f"DELETE FROM productos WHERE id IN ({','.join(['?']*len(target_ids))})", target_ids)
conn.commit()

print(f"Registros eliminados: {target_ids}")
conn.close()
