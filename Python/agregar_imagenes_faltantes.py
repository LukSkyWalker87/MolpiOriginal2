import sqlite3
from datetime import datetime

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print("=== AGREGANDO IMÁGENES A PRODUCTOS SIN IMAGEN ===")

# Mapeo de productos a sus imágenes correspondientes
productos_imagenes = [
    (69, 'Vainilla de 3', 'img/products/vainilla_de_3_molde.jpg'),
    (70, 'Vainilla de 4', 'img/products/vainilla_de_4_molde.jpg'),
    (71, '9 Panes', 'img/products/9_panes_molde.jpg'),
    (72, 'Laja 20x20', 'img/products/laja_20_molde.jpg'),
    (73, 'Liso 20x20', 'img/products/lisa_20_molde.jpg')
]

for producto_id, nombre, imagen_url in productos_imagenes:
    c.execute("""
        UPDATE productos 
        SET imagen_url = ?, fecha_modificacion = ?
        WHERE id = ?
    """, (imagen_url, fecha_actual, producto_id))
    print(f"✅ {nombre} -> {imagen_url}")

conn.commit()

print("\n=== VERIFICANDO RESULTADO ===")
c.execute("""
    SELECT id, nombre, imagen_url 
    FROM productos 
    WHERE categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20' 
    ORDER BY nombre
""")

productos_actualizados = c.fetchall()
for p in productos_actualizados:
    print(f"ID {p[0]}: {p[1]} -> {p[2] if p[2] else 'SIN IMAGEN'}")

conn.close()
print("\n¡Imágenes agregadas correctamente!")
