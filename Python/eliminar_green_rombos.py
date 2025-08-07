import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔍 Buscando el producto 'Green Rombos'...")
    
    # Primero verificar que existe el producto
    cursor.execute('''
        SELECT id, nombre, categoria, activo 
        FROM productos 
        WHERE nombre = 'Green Rombos'
    ''')
    producto = cursor.fetchone()
    
    if producto:
        producto_id, nombre, categoria, activo = producto
        print(f"📦 Producto encontrado:")
        print(f"   ID: {producto_id}")
        print(f"   Nombre: {nombre}")
        print(f"   Categoría: {categoria}")
        print(f"   Activo: {activo}")
        
        # Confirmar eliminación
        print(f"\n⚠️  ¿Estás seguro de que quieres eliminar PERMANENTEMENTE el producto '{nombre}'?")
        print("   Esta acción NO se puede deshacer.")
        
        # Eliminar el producto
        cursor.execute('''
            DELETE FROM productos 
            WHERE nombre = 'Green Rombos'
        ''')
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Producto '{nombre}' eliminado permanentemente de la base de datos")
            print(f"   Registros eliminados: {cursor.rowcount}")
        else:
            print("❌ No se pudo eliminar el producto")
    else:
        print("❌ No se encontró el producto 'Green Rombos' en la base de datos")
    
    # Verificar que se eliminó correctamente
    print("\n🔍 Verificando eliminación...")
    cursor.execute('''
        SELECT COUNT(*) 
        FROM productos 
        WHERE nombre = 'Green Rombos'
    ''')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("✅ Confirmado: El producto ya no existe en la base de datos")
    else:
        print(f"⚠️  Advertencia: Aún se encontraron {count} registros con ese nombre")
    
    # Mostrar productos Green restantes
    print("\n📋 Productos Green restantes:")
    cursor.execute('''
        SELECT id, nombre, activo 
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY nombre
    ''')
    productos_restantes = cursor.fetchall()
    
    if productos_restantes:
        for producto in productos_restantes:
            estado = "Activo" if producto[2] else "Inactivo"
            print(f"   • {producto[1]} (ID: {producto[0]}) - {estado}")
    else:
        print("   No hay productos Green en la base de datos")

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")
    conn.rollback()

finally:
    conn.close()
    print("\n🔒 Conexión cerrada")
