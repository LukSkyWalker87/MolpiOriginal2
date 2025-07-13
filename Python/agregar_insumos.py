import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print('📁 Agregando productos de Insumos...')

insumos = [
    ('Desmoldante 1L', 'Desmoldante líquido para fácil extracción', 'Insumos', 'Herramientas', 800.0),
    ('Colorante Rojo', 'Colorante óxido rojo para cemento', 'Insumos', 'Materiales', 350.0),
    ('Colorante Amarillo', 'Colorante óxido amarillo para cemento', 'Insumos', 'Materiales', 350.0),
    ('Colorante Negro', 'Colorante óxido negro para cemento', 'Insumos', 'Materiales', 380.0),
    ('Cemento Blanco 1kg', 'Cemento blanco especial para moldeo', 'Insumos', 'Materiales', 450.0),
    ('Arena Fina 25kg', 'Arena fina seleccionada para moldeo', 'Insumos', 'Materiales', 600.0),
    ('Kit Iniciación', 'Kit completo para empezar', 'Insumos', 'Materiales', 2500.0)
]

for nombre, desc, cat, subcat, precio in insumos:
    c.execute("""
        INSERT OR IGNORE INTO productos (nombre, descripcion, categoria, subcategoria, precio, activo) 
        VALUES (?, ?, ?, ?, ?, 1)
    """, (nombre, desc, cat, subcat, precio))
    print(f'   ✅ {nombre} agregado')

conn.commit()

print('\n📊 Resumen final:')
c.execute('SELECT categoria, COUNT(*) FROM productos GROUP BY categoria ORDER BY categoria')
for categoria, count in c.fetchall():
    print(f'   • {categoria}: {count} productos')

conn.close()
print('\n✅ ¡Insumos agregados correctamente!')
