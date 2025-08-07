import sqlite3
import os

# Configurar la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar testimonios
    cursor.execute('SELECT id, nombre, empresa, testimonio, fecha_creacion FROM testimonios ORDER BY id DESC LIMIT 10')
    testimonios = cursor.fetchall()
    
    print('Últimos 10 testimonios en la BD:')
    for t in testimonios:
        print(f'ID: {t[0]}, Nombre: {t[1]}, Empresa: {t[2]}, Fecha: {t[4]}')
        print(f'   Testimonio: {t[3][:80]}...')
        print('---')
    
    # Buscar duplicados por contenido
    cursor.execute('''
        SELECT nombre, empresa, testimonio, COUNT(*) as count 
        FROM testimonios 
        GROUP BY nombre, empresa, testimonio 
        HAVING COUNT(*) > 1
    ''')
    duplicados = cursor.fetchall()
    
    if duplicados:
        print('\n🚨 DUPLICADOS ENCONTRADOS:')
        for dup in duplicados:
            print(f'   {dup[0]} - {dup[1]}: {dup[3]} veces')
    else:
        print('\n✅ No hay duplicados en la base de datos')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
