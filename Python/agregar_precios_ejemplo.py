import sqlite3

conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Agregar precios de ejemplo a algunos productos
productos_ejemplo = [
    (98, 15000, 85),    # Laja San Juan
    (99, 18000, 95),    # Adoquín Colonial  
    (100, 22000, 120),  # Deck Símil Madera
    (101, 20000, 110),  # Deck Antideslizante
    (102, 25000, 135),  # Madera 50x25x6
    (103, 12000, 70),   # Liso
    (104, 17000, 90),   # Quebracho
    (105, 16000, 85)    # Corteza
]

print("Actualizando precios de ejemplo...")
for producto_id, precio_ars, precio_usd in productos_ejemplo:
    cursor.execute("""
        UPDATE productos 
        SET precio = ?, precio_usd = ?
        WHERE id = ?
    """, (precio_ars, precio_usd, producto_id))
    print(f"Producto ID {producto_id}: ${precio_ars} ARS / U$D {precio_usd}")

conn.commit()

# Verificar los cambios
cursor.execute("""
    SELECT id, nombre, precio, precio_usd 
    FROM productos 
    WHERE id IN (98, 99, 100, 101, 102, 103, 104, 105)
    ORDER BY id
""")
productos = cursor.fetchall()

print("\nVerificación de precios actualizados:")
for producto in productos:
    id_prod, nombre, precio_ars, precio_usd = producto
    print(f"ID {id_prod}: {nombre} - ${precio_ars} ARS / U$D {precio_usd}")

conn.close()
print("\n✅ Precios actualizados correctamente!")
