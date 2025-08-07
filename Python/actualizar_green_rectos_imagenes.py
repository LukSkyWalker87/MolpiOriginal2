import sqlite3
import os

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Actualizar las URLs de imágenes para Green Rectos
    cursor.execute('''
        UPDATE productos 
        SET imagen_url = ?, imagen_mosaico_url = ?
        WHERE nombre = ? AND categoria = ?
    ''', (
        'img/products/recto_green_molde.jpg',
        'img/products/recto_green_mosaico.png',
        'Green Rectos',
        'Green'
    ))
    
    # Confirmar cambios
    conn.commit()
    
    # Verificar el número de filas afectadas
    rows_affected = cursor.rowcount
    print(f"✅ Filas actualizadas: {rows_affected}")
    
    if rows_affected > 0:
        print("✅ Producto Green Rectos actualizado con las nuevas imágenes")
        
        # Verificar que se actualizó correctamente
        cursor.execute('''
            SELECT id, nombre, imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE nombre = ? AND categoria = ?
        ''', ('Green Rectos', 'Green'))
        
        producto = cursor.fetchone()
        
        if producto:
            print(f"📦 Producto verificado:")
            print(f"   - ID: {producto[0]}")
            print(f"   - Nombre: {producto[1]}")
            print(f"   - Imagen molde: {producto[2]}")
            print(f"   - Imagen mosaico: {producto[3]}")
    else:
        print("❌ No se encontró el producto Green Rectos para actualizar")
        
        # Buscar productos similares
        cursor.execute('''
            SELECT id, nombre, categoria 
            FROM productos 
            WHERE categoria = 'Green'
            ORDER BY nombre
        ''')
        productos = cursor.fetchall()
        
        print("\n🔍 Productos Green disponibles:")
        for p in productos:
            print(f"   - ID: {p[0]}, Nombre: '{p[1]}', Categoría: {p[2]}")

except sqlite3.Error as e:
    print(f"❌ Error al actualizar producto: {e}")

finally:
    conn.close()

print("\n🔄 Verificando productos Green actualizados...")

# Verificar todos los productos Green
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    SELECT id, nombre, imagen_url, imagen_mosaico_url, activo 
    FROM productos 
    WHERE categoria = 'Green' 
    ORDER BY nombre
''')
productos_green = cursor.fetchall()

print("📋 Estado actual de productos Green:")
for producto in productos_green:
    estado = "✅ Activo" if producto[4] == 1 else "❌ Inactivo"
    imagen_molde = "✅" if producto[2] else "❌"
    imagen_mosaico = "✅" if producto[3] else "❌"
    print(f"- ID: {producto[0]}, Nombre: '{producto[1]}', {estado}")
    print(f"  Molde: {imagen_molde} | Mosaico: {imagen_mosaico}")

conn.close()
