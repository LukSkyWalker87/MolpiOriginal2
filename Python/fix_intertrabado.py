import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔄 Actualizando imágenes de Intertrabado...")
    
    # Actualizar específicamente el producto Intertrabado
    cursor.execute('''
        UPDATE productos 
        SET imagen_url = ?, imagen_mosaico_url = ?
        WHERE nombre = 'Intertrabado' AND categoria = 'Green'
    ''', (
        'img/products/intertrabado_molde.jpg',
        'img/products/intertrabado_mosaico.jpg'
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
        
        print("\n📦 Productos Intertrabado actualizados:")
        for producto in productos:
            print(f"   ID: {producto[0]}")
            print(f"   Nombre: {producto[1]}")
            print(f"   Imagen molde: {producto[2]}")
            print(f"   Imagen mosaico: {producto[3]}")
            print()
    else:
        print("❌ No se encontró el producto Intertrabado para actualizar")

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")

finally:
    conn.close()
    print("🔒 Conexión cerrada")
