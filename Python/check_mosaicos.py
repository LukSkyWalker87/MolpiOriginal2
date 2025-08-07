import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Verificar productos 20x20 con mosaicos
c.execute('''
    SELECT id, nombre, imagen_url, imagen_mosaico_url 
    FROM productos 
    WHERE categoria = "Pisos y Zócalos" AND subcategoria = "Línea 20x20" 
    ORDER BY nombre
''')

productos = c.fetchall()
print('Productos 20x20:')
print('-' * 80)
for p in productos:
    print(f'ID: {p[0]:<3} | Nombre: {p[1]:<25} | Molde: {p[2] or "Sin molde":<35} | Mosaico: {p[3] or "Sin mosaico"}')

conn.close()
