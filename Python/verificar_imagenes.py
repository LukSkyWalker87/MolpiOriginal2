import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("=== VERIFICANDO IMÁGENES EN PRODUCTOS LÍNEA 20x20 ===")
c.execute("""
    SELECT id, nombre, imagen_url, categoria, subcategoria 
    FROM productos 
    WHERE categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20' 
    ORDER BY id
""")

productos = c.fetchall()
for p in productos:
    print(f"ID {p[0]}: {p[1]}")
    print(f"  Imagen URL: {p[2] if p[2] else 'NULL/VACÍO'}")
    print(f"  Categoría: {p[3]} / {p[4]}")
    print()

print("=== VERIFICANDO TODAS LAS IMÁGENES EN PRODUCTOS ===")
c.execute("SELECT id, nombre, imagen_url FROM productos WHERE imagen_url IS NOT NULL AND imagen_url != '' ORDER BY id")
productos_con_imagen = c.fetchall()
print(f"Total productos con imagen: {len(productos_con_imagen)}")
for p in productos_con_imagen:
    print(f"ID {p[0]}: {p[1]} -> {p[2]}")

conn.close()
