import sqlite3

# IDs a eliminar (puedes modificar esta lista si necesitas borrar otros)
IDS_A_BORRAR = [158, 159, 160, 161]

DB_PATH = 'OLD/molpi_Python.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

for id_ in IDS_A_BORRAR:
    c.execute('DELETE FROM productos WHERE id = ?', (id_,))
    print(f'Intentando borrar producto con id={id_}')

conn.commit()

# Verificar si siguen existiendo
c.execute('SELECT id FROM productos WHERE id IN ({})'.format(','.join(['?']*len(IDS_A_BORRAR))), IDS_A_BORRAR)
restantes = c.fetchall()
if restantes:
    print('Aún existen los siguientes IDs:', [r[0] for r in restantes])
else:
    print('Todos los productos fueron eliminados correctamente.')

conn.close()
