import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Mapeo de productos con sus imágenes de mosaico
# Basado en los productos obtenidos de la API: /productos/linea/50x50
productos_mosaico_50x50 = {
    "Laja San Juan": "img/products/laja_san_juan_mosaico.png",
    "Adoquín Colonial": "img/products/laja_colonial_mosaico.png",  # Asumo que es el colonial
    "Deck Símil Madera": "img/products/deck_simil_madera_mosaico.png",
    "Deck Antideslizante": "img/products/deck_antideslizante_mosaico.png",
    "Madera 50x25x6 / 2 piezas por molde": "img/products/madera_6_cm_mosaico.png",
    "Liso": "img/products/liso_mosaico.png",
    "Quebracho": "img/products/quebracho_mosaico.png",
    "Corteza": "img/products/corteza_mosaico.png"
}

print("=== ACTUALIZACIÓN DE MOSAICOS LÍNEA 50x50 ===")
print(f"Productos a actualizar: {len(productos_mosaico_50x50)}")
print()

# Obtener productos actuales de la línea 50x50
cursor.execute("""
    SELECT id, nombre 
    FROM productos 
    WHERE id IN (98, 99, 100, 101, 102, 103, 104, 105)
    ORDER BY id
""")
productos_db = cursor.fetchall()

actualizaciones_exitosas = 0
productos_no_encontrados = []

for producto_id, nombre_db in productos_db:
    print(f"Procesando: ID {producto_id} - {nombre_db}")
    
    # Buscar la imagen correspondiente
    imagen_mosaico = None
    for nombre_mosaico, ruta_imagen in productos_mosaico_50x50.items():
        if nombre_mosaico.lower() in nombre_db.lower() or nombre_db.lower() in nombre_mosaico.lower():
            imagen_mosaico = ruta_imagen
            break
    
    if imagen_mosaico:
        # Actualizar el producto con la imagen de mosaico
        cursor.execute("""
            UPDATE productos 
            SET imagen_mosaico_url = ? 
            WHERE id = ?
        """, (imagen_mosaico, producto_id))
        
        print(f"  ✅ Actualizado con: {imagen_mosaico}")
        actualizaciones_exitosas += 1
    else:
        print(f"  ❌ No se encontró imagen para: {nombre_db}")
        productos_no_encontrados.append(nombre_db)

# Confirmar cambios
conn.commit()

print()
print("=== RESUMEN ===")
print(f"Actualizaciones exitosas: {actualizaciones_exitosas}")
print(f"Productos no encontrados: {len(productos_no_encontrados)}")

if productos_no_encontrados:
    print("\nProductos sin imagen asignada:")
    for producto in productos_no_encontrados:
        print(f"  - {producto}")

# Verificar resultados
print("\n=== VERIFICACIÓN FINAL ===")
cursor.execute("""
    SELECT id, nombre, imagen_mosaico_url 
    FROM productos 
    WHERE id IN (98, 99, 100, 101, 102, 103, 104, 105)
    ORDER BY id
""")
productos_verificacion = cursor.fetchall()

for producto_id, nombre, mosaico_url in productos_verificacion:
    estado = "✅ CON MOSAICO" if mosaico_url else "❌ SIN MOSAICO"
    print(f"ID {producto_id}: {nombre} - {estado}")

conn.close()
print("\n🎉 Actualización completada!")
