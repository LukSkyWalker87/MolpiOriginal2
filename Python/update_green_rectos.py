import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔍 Buscando productos Green...")
    
    # Buscar todos los productos Green
    cursor.execute('''
        SELECT id, nombre, categoria, imagen_url, imagen_mosaico_url, activo 
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY nombre
    ''')
    productos = cursor.fetchall()
    
    print(f"📋 Productos Green encontrados: {len(productos)}")
    for p in productos:
        estado = "✅ Activo" if p[5] == 1 else "❌ Inactivo"
        print(f"- ID: {p[0]}, Nombre: '{p[1]}', {estado}")
        print(f"  Imagen molde: {p[3] or 'Sin imagen'}")
        print(f"  Imagen mosaico: {p[4] or 'Sin imagen'}")
        print()
    
    # Buscar específicamente Green Rectos
    cursor.execute('''
        SELECT id, nombre, imagen_url, imagen_mosaico_url 
        FROM productos 
        WHERE nombre = 'Green Rectos'
    ''')
    green_rectos = cursor.fetchone()
    
    if green_rectos:
        print(f"🎯 Green Rectos encontrado - ID: {green_rectos[0]}")
        print(f"   Imagen molde actual: {green_rectos[2] or 'Sin imagen'}")
        print(f"   Imagen mosaico actual: {green_rectos[3] or 'Sin imagen'}")
        
        # Actualizar las imágenes
        print("\n🔄 Actualizando imágenes de Green Rectos...")
        cursor.execute('''
            UPDATE productos 
            SET imagen_url = ?, imagen_mosaico_url = ?
            WHERE id = ?
        ''', (
            'img/products/recto_green_molde.jpg',
            'img/products/recto_green_mosaico.png',
            green_rectos[0]
        ))
        
        conn.commit()
        print("✅ Imágenes actualizadas exitosamente")
        
        # Verificar la actualización
        cursor.execute('''
            SELECT imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE id = ?
        ''', (green_rectos[0],))
        updated = cursor.fetchone()
        
        print(f"📸 Nueva imagen molde: {updated[0]}")
        print(f"📸 Nueva imagen mosaico: {updated[1]}")
        
    else:
        print("❌ No se encontró el producto Green Rectos")

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")

finally:
    conn.close()
    print("\n🔒 Conexión a base de datos cerrada")
