import sqlite3
import os

# Configurar la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar tablas disponibles
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print('Tablas disponibles:', [table[0] for table in tables])
    
    # Verificar productos
    cursor.execute('SELECT COUNT(*) FROM productos')
    count = cursor.fetchone()[0]
    print(f'Total productos en la BD: {count}')
    
    # Verificar algunas categorías
    cursor.execute('SELECT DISTINCT categoria FROM productos LIMIT 10')
    categorias = cursor.fetchall()
    print('Categorías encontradas:', [cat[0] for cat in categorias])
    
    # Verificar primeros 3 productos
    cursor.execute('SELECT id, nombre, categoria FROM productos LIMIT 3')
    productos = cursor.fetchall()
    print('Primeros 3 productos:')
    for prod in productos:
        print(f'  ID: {prod[0]}, Nombre: {prod[1]}, Categoría: {prod[2]}')
    
    conn.close()
    print('\n✅ Base de datos accesible correctamente')
    
except Exception as e:
    print(f'❌ Error al acceder a la base de datos: {e}')
