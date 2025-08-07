import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔧 Corrigiendo rutas de imágenes Intertrabado...")
    
    # Actualizar con los nombres correctos de archivos que SÍ existen
    cursor.execute('''
        UPDATE productos 
        SET imagen_url = ?, imagen_mosaico_url = ?
        WHERE nombre = 'Intertrabado' AND categoria = 'Green'
    ''', (
        'img/products/intertrabado.jpg',          # Este archivo SÍ existe
        'img/products/intertrabado_mosaico.png'   # Este archivo SÍ existe
    ))
    
    # Confirmar cambios
    conn.commit()
    rows_affected = cursor.rowcount
    
    if rows_affected > 0:
        print(f"✅ {rows_affected} producto(s) Intertrabado actualizado(s)")
        
        # Verificar la actualización
        cursor.execute('''
            SELECT id, nombre, imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE nombre = 'Intertrabado' AND categoria = 'Green'
        ''')
        productos = cursor.fetchall()
        
        print("\n📦 Productos Intertrabado con rutas corregidas:")
        for producto in productos:
            print(f"   ID: {producto[0]}")
            print(f"   Nombre: {producto[1]}")
            print(f"   Imagen molde: {producto[2]}")
            print(f"   Imagen mosaico: {producto[3]}")
            print()
            
        # Verificar que las imágenes ahora sean accesibles
        import requests
        base_url = "http://127.0.0.1:5000/"
        
        for producto in productos:
            if producto[2]:  # imagen_url
                try:
                    response = requests.head(base_url + producto[2])
                    status = f"✅ {response.status_code}" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   Verificación molde: {status}")
                except Exception as e:
                    print(f"   Verificación molde: ❌ Error: {e}")
            
            if producto[3]:  # imagen_mosaico_url
                try:
                    response = requests.head(base_url + producto[3])
                    status = f"✅ {response.status_code}" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   Verificación mosaico: {status}")
                except Exception as e:
                    print(f"   Verificación mosaico: ❌ Error: {e}")
    else:
        print("❌ No se encontró el producto Intertrabado para actualizar")

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")

finally:
    conn.close()
    print("🔒 Conexión cerrada")
