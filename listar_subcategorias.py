import sqlite3

conn = sqlite3.connect('backend/molpi.db')
c = conn.cursor()

print('Subcategorías en la base de datos:')
for row in c.execute('SELECT id, nombre, categoria_id FROM subcategorias'):
    print(row)

print('\nCategorías en la base de datos:')
for row in c.execute('SELECT id, nombre FROM categorias'):
    print(row)

conn.close()
