import sqlite3
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print('=== CATEGORÍAS Y SUBCATEGORÍAS ===')
c.execute('SELECT DISTINCT categoria, subcategoria FROM productos ORDER BY categoria, subcategoria')
categorias = c.fetchall()
for cat in categorias:
    print(f'Categoría: {cat[0]} | Subcategoría: {cat[1]}')

print('\n=== PRODUCTOS QUE CONTIENEN 40 ===')
c.execute('SELECT id, nombre, categoria, subcategoria FROM productos WHERE nombre LIKE "%40%" OR categoria LIKE "%40%" OR subcategoria LIKE "%40%" ORDER BY nombre')
productos_40 = c.fetchall()
for prod in productos_40:
    print(f'ID: {prod[0]} | {prod[1]} | Cat: {prod[2]} | Sub: {prod[3]}')

conn.close()
