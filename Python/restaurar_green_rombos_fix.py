import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔍 Verificando estructura de la tabla productos...")
    
    # Obtener información de la tabla
    cursor.execute("PRAGMA table_info(productos)")
    columnas = cursor.fetchall()
    
    print("📋 Columnas de la tabla productos:")
    for col in columnas:
        print(f"   {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
    
    print("\n🔄 Restaurando Green Rombos con la estructura correcta...")
    
    # Insertar con solo las columnas que existen
    cursor.execute('''
        INSERT INTO productos (
            nombre, descripcion, precio, categoria, activo, 
            imagen_url, imagen_mosaico_url
        ) VALUES (
            'Green Rombos',
            'Molde para baldosas con diseño de rombo ecológico...',
            1850.00,
            'Green',
            1,
            'img/products/rombo_green_molde.jpg',
            'img/products/rombo_green_mosaico.png'
        )
    ''')
    
    conn.commit()
    nuevo_id = cursor.lastrowid
    print(f"✅ Green Rombos restaurado exitosamente con ID: {nuevo_id}")
    
    # Verificar el resultado
    print("\n📋 Productos Green actualizados:")
    cursor.execute('''
        SELECT id, nombre, activo, imagen_url, imagen_mosaico_url
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY nombre
    ''')
    productos = cursor.fetchall()
    
    for producto in productos:
        print(f"📦 {producto[1]} (ID: {producto[0]}) - {'Activo' if producto[2] else 'Inactivo'}")
        print(f"   Molde: {producto[3] or 'Sin imagen'}")
        print(f"   Mosaico: {producto[4] or 'Sin imagen'}")
        print()

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")
    conn.rollback()

finally:
    conn.close()
    print("🔒 Conexión cerrada")
