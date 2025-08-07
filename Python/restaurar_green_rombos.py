import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔍 Verificando estado actual de productos Green...")
    
    # Verificar productos Green actuales
    cursor.execute('''
        SELECT id, nombre, categoria, activo, imagen_url, imagen_mosaico_url
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY id
    ''')
    productos_actuales = cursor.fetchall()
    
    print(f"📋 Productos Green encontrados: {len(productos_actuales)}")
    for producto in productos_actuales:
        print(f"   ID: {producto[0]}, Nombre: {producto[1]}, Activo: {producto[2]}")
        print(f"      Molde: {producto[4] or 'Sin imagen'}")
        print(f"      Mosaico: {producto[5] or 'Sin imagen'}")
        print()
    
    print("🔄 Restaurando el producto Green Rombos que estaba bien...")
    
    # Restaurar el producto Green Rombos con los datos correctos
    cursor.execute('''
        INSERT INTO productos (
            nombre, descripcion, precio, categoria, activo, 
            imagen_url, imagen_mosaico_url, created_at, updated_at
        ) VALUES (
            'Green Rombos',
            'Molde para baldosas con diseño de rombo ecológico...',
            1850.00,
            'Green',
            1,
            'img/products/rombo_green_molde.jpg',
            'img/products/rombo_green_mosaico.png',
            datetime('now'),
            datetime('now')
        )
    ''')
    
    # Confirmar cambios
    conn.commit()
    
    # Obtener el ID del producto insertado
    nuevo_id = cursor.lastrowid
    print(f"✅ Producto Green Rombos restaurado con ID: {nuevo_id}")
    
    # Verificar el resultado final
    print("\n🔍 Estado final de productos Green:")
    cursor.execute('''
        SELECT id, nombre, categoria, activo, imagen_url, imagen_mosaico_url
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY nombre
    ''')
    productos_finales = cursor.fetchall()
    
    for producto in productos_finales:
        print(f"📦 {producto[1]} (ID: {producto[0]}) - {'Activo' if producto[3] else 'Inactivo'}")
        print(f"   Molde: {producto[4] or 'Sin imagen'}")
        print(f"   Mosaico: {producto[5] or 'Sin imagen'}")
        print()

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")
    conn.rollback()

finally:
    conn.close()
    print("🔒 Conexión cerrada")
