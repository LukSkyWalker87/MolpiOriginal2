import sqlite3

# Lista de productos 50x50 especificados por el usuario
productos_50x50 = [
    "Laja San Juan",
    "Adoquín Colonial",
    "Deck Símil Madera",
    "Deck Antideslizante", 
    "Madera 50x25x6 / 2 piezas por molde",
    "Liso",
    "Quebracho",
    "Corteza"
]

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

print("Agregando productos de la línea 50x50...")

# Obtener el ID más alto actual
cursor.execute("SELECT MAX(id) FROM productos")
max_id = cursor.fetchone()[0] or 0

for i, nombre in enumerate(productos_50x50):
    nuevo_id = max_id + i + 1
    
    # Generar URL de imagen basada en el nombre
    imagen_url = f"img/products/{nombre.lower().replace(' ', '_').replace('/', '_').replace('.', '').replace('°', '').replace('ñ', 'n')}_molde.jpg"
    
    # Insertar producto
    cursor.execute("""
        INSERT INTO productos (id, nombre, descripcion, precio, imagen_url, subcategoria)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        nuevo_id,
        nombre,
        f"Molde para {nombre.lower()}",
        0.0,
        imagen_url,
        "Línea 50x50"
    ))
    
    print(f"Agregado: {nuevo_id} - {nombre}")

# Confirmar cambios
conn.commit()

# Verificar productos agregados
print("\nProductos de la línea 50x50 en la base de datos:")
cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
productos = cursor.fetchall()

for producto in productos:
    print(f"ID: {producto[0]}, Nombre: {producto[1]}, URL: {producto[2]}")

print(f"\nTotal productos 50x50: {len(productos)}")

conn.close()
