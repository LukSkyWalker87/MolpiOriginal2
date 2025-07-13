import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Verificar las categorías y subcategorías exactas
print('=== CATEGORÍAS ÚNICAS ===')
c.execute('SELECT DISTINCT categoria FROM productos WHERE activo = 1')
for row in c.fetchall():
    print(f'Categoria: "{row[0]}" (len={len(row[0])})')

print('\n=== SUBCATEGORÍAS ÚNICAS ===')
c.execute('SELECT DISTINCT subcategoria FROM productos WHERE activo = 1')
for row in c.fetchall():
    print(f'Subcategoria: "{row[0]}" (len={len(row[0])})')
    
print('\n=== PRODUCTOS POR CATEGORÍA ===')
c.execute('SELECT categoria, COUNT(*) FROM productos WHERE activo = 1 GROUP BY categoria')
for row in c.fetchall():
    print(f'{row[0]}: {row[1]} productos')

print('\n=== PRODUCTOS POR SUBCATEGORÍA ===')
c.execute('SELECT subcategoria, COUNT(*) FROM productos WHERE activo = 1 GROUP BY subcategoria')
for row in c.fetchall():
    print(f'{row[0]}: {row[1]} productos')

# Verificar productos específicos de "Pisos y Zócalos"
print('\n=== PRODUCTOS DE "Pisos y Zócalos" ===')
c.execute('SELECT nombre, categoria, subcategoria FROM productos WHERE categoria = "Pisos y Zócalos" AND activo = 1')
for row in c.fetchall():
    print(f'Nombre: "{row[0]}", Categoria: "{row[1]}", Subcategoria: "{row[2]}"')

conn.close()
