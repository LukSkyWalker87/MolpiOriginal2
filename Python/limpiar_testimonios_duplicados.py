import sqlite3
import os

# Configurar la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print('🧹 Limpiando testimonios duplicados...')
    
    # Buscar duplicados (mantener el más reciente)
    cursor.execute('''
        DELETE FROM testimonios 
        WHERE id NOT IN (
            SELECT MAX(id) 
            FROM testimonios 
            GROUP BY nombre, empresa, testimonio
        )
    ''')
    
    eliminados = cursor.rowcount
    conn.commit()
    
    print(f'✅ Eliminados {eliminados} testimonios duplicados')
    
    # Verificar resultado
    cursor.execute('SELECT id, nombre, empresa, testimonio, fecha_creacion FROM testimonios ORDER BY id')
    testimonios = cursor.fetchall()
    
    print(f'\n📊 Testimonios restantes ({len(testimonios)}):')
    for t in testimonios:
        print(f'ID: {t[0]}, {t[1]} - {t[2]}, Fecha: {t[4]}')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
