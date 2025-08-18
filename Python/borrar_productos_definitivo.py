import sqlite3

# Ruta real de la base de datos usada por el backend
DB_PATH = r'C:\tmp\molpi.db'

# IDs a eliminar (los que aparecen en la imagen)
IDS_A_ELIMINAR = [162, 160, 161, 158, 159]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for id_ in IDS_A_ELIMINAR:
    c.execute('DELETE FROM productos WHERE id = ?', (id_,))
    print(f"Eliminado producto con id {id_}")

conn.commit()
conn.close()
print("Eliminación completada.")
