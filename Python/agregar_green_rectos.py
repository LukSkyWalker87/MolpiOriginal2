import sqlite3
import os

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Datos del producto Green Rectos
producto_data = {
    'nombre': 'Green Rectos',
    'categoria': 'Green',
    'descripcion': 'Molde Green Rectos con diseño numeral. Aptos para entradas vehiculares o peatonales, dando un aspecto muy agradable y confortable entre espacio verde y el cemento gris.',
    'precio': 15000.0,
    'precio_usd': 15.0,
    'activo': 1,
    'imagen_url': 'img/green_rectos.jpg',
    'imagen_mosaico_url': 'img/green_rectos_mosaico.jpg'
}

try:
    # Insertar el nuevo producto
    cursor.execute('''
        INSERT INTO productos (nombre, categoria, descripcion, precio, precio_usd, activo, imagen_url, imagen_mosaico_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        producto_data['nombre'],
        producto_data['categoria'], 
        producto_data['descripcion'],
        producto_data['precio'],
        producto_data['precio_usd'],
        producto_data['activo'],
        producto_data['imagen_url'],
        producto_data['imagen_mosaico_url']
    ))
    
    # Confirmar cambios
    conn.commit()
    
    # Obtener el ID del producto insertado
    producto_id = cursor.lastrowid
    
    print(f"✅ Producto Green Rectos agregado exitosamente con ID: {producto_id}")
    
    # Verificar que se agregó correctamente
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()
    
    if producto:
        print(f"📦 Producto verificado:")
        print(f"   - ID: {producto[0]}")
        print(f"   - Nombre: {producto[1]}")
        print(f"   - Categoría: {producto[2]}")
        print(f"   - Activo: {producto[6]}")

except sqlite3.Error as e:
    print(f"❌ Error al agregar producto: {e}")

finally:
    conn.close()

print("\n🔍 Verificando productos Green actuales...")

# Verificar todos los productos Green
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT id, nombre, categoria, activo FROM productos WHERE categoria = 'Green' ORDER BY nombre")
productos_green = cursor.fetchall()

print("Productos Green en la base de datos:")
for producto in productos_green:
    estado = "✅ Activo" if producto[3] == 1 else "❌ Inactivo"
    print(f"- ID: {producto[0]}, Nombre: '{producto[1]}', {estado}")

conn.close()
