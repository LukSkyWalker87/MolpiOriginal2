import sqlite3

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Mapeo correcto de imágenes según las attachments
productos_imagenes = {
    'Green Rombos': {
        'molde': 'img/products/rombo_green_molde.jpg',
        'mosaico': 'img/products/rombo_green_mosaico.png'
    },
    'Círculos Green': {
        'molde': 'img/products/circulos_green_molde.jpg', 
        'mosaico': 'img/products/circulos_green_mosaico.png'
    },
    'Green Rectos': {
        'molde': 'img/products/recto_green_molde.jpg',
        'mosaico': 'img/products/recto_green_mosaico.png'
    },
    'Adoquín Individual': {
        'molde': 'img/products/adoquin_individual_molde.jpg',
        'mosaico': 'img/products/adoquin_individual_mosaico.png'
    },
    'Intertrabado': {
        'molde': 'img/products/intertrabado_molde.jpg',
        'mosaico': 'img/products/intertrabado_mosaico.jpg'
    }
}

try:
    print("🔄 Actualizando imágenes de productos Green...")
    
    # Obtener todos los productos Green
    cursor.execute('''
        SELECT id, nombre FROM productos 
        WHERE categoria = 'Green' AND activo = 1
        ORDER BY nombre
    ''')
    productos = cursor.fetchall()
    
    print(f"📋 Productos Green encontrados: {len(productos)}")
    
    for producto_id, nombre in productos:
        if nombre in productos_imagenes:
            imagenes = productos_imagenes[nombre]
            
            # Actualizar las imágenes
            cursor.execute('''
                UPDATE productos 
                SET imagen_url = ?, imagen_mosaico_url = ?
                WHERE id = ?
            ''', (imagenes['molde'], imagenes['mosaico'], producto_id))
            
            print(f"✅ {nombre} (ID: {producto_id})")
            print(f"   Molde: {imagenes['molde']}")
            print(f"   Mosaico: {imagenes['mosaico']}")
        else:
            print(f"⚠️  {nombre} (ID: {producto_id}) - No se encontró mapeo de imágenes")
    
    # Confirmar cambios
    conn.commit()
    print("\n✅ Todas las imágenes han sido actualizadas")
    
    # Verificar el resultado
    print("\n🔍 Verificando productos actualizados:")
    cursor.execute('''
        SELECT id, nombre, imagen_url, imagen_mosaico_url 
        FROM productos 
        WHERE categoria = 'Green' AND activo = 1
        ORDER BY nombre
    ''')
    productos_verificados = cursor.fetchall()
    
    for producto in productos_verificados:
        print(f"📦 {producto[1]} (ID: {producto[0]})")
        print(f"   Molde: {producto[2] or 'Sin imagen'}")
        print(f"   Mosaico: {producto[3] or 'Sin imagen'}")
        print()

except sqlite3.Error as e:
    print(f"❌ Error de base de datos: {e}")

finally:
    conn.close()
    print("🔒 Conexión cerrada")
