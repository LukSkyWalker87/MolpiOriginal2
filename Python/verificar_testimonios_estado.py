import sqlite3
import os

# Configurar la ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar todos los testimonios
    cursor.execute('SELECT id, nombre, empresa, activo, orden FROM testimonios ORDER BY orden')
    testimonios = cursor.fetchall()
    
    print('📊 Todos los testimonios en la BD:')
    for t in testimonios:
        estado = "✅ Activo" if t[3] else "❌ Inactivo"
        print(f'ID: {t[0]}, {t[1]} - {t[2]}, {estado}, Orden: {t[4]}')
    
    print(f'\nTotal: {len(testimonios)} testimonios')
    
    # Verificar solo activos (los que aparecerían en la página)
    cursor.execute('SELECT id, nombre, empresa, orden FROM testimonios WHERE activo = 1 ORDER BY orden')
    activos = cursor.fetchall()
    
    print(f'\n🟢 Testimonios ACTIVOS ({len(activos)}):')
    for t in activos:
        print(f'  {t[1]} - {t[2]} (Orden: {t[3]})')
    
    conn.close()
    
except Exception as e:
    print(f'❌ Error: {e}')
