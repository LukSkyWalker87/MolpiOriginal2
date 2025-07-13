import sqlite3

def limpiar_y_corregir_datos():
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    print("Limpiando datos incorrectos...")
    
    # Eliminar todos los productos existentes
    c.execute("DELETE FROM productos")
    
    # Insertar productos correctos de ejemplo para la línea 20x20
    productos_correctos = [
        {
            'nombre': 'Vainilla de 5',
            'descripcion': 'Molde para baldosas con diseño vainilla de 5 cm',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/vainilla5.jpg',
            'pdf_url': 'pdf/vainilla5.pdf',
            'precio': 1500.00
        },
        {
            'nombre': 'Vainilla de 6',
            'descripcion': 'Molde para baldosas con diseño vainilla de 6 cm',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/vainilla6.jpg',
            'pdf_url': 'pdf/vainilla6.pdf',
            'precio': 1650.00
        },
        {
            'nombre': 'Adoquín Rústico',
            'descripcion': 'Molde para baldosas con diseño de adoquín rústico',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/adoquin.jpg',
            'pdf_url': 'pdf/adoquin.pdf',
            'precio': 1800.00
        },
        {
            'nombre': 'Piedra París',
            'descripcion': 'Molde para baldosas con diseño símil piedra París',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/piedra_paris.jpg',
            'pdf_url': 'pdf/piedra_paris.pdf',
            'precio': 1750.00
        },
        {
            'nombre': 'Ladrillo Colonial',
            'descripcion': 'Molde para baldosas con diseño de ladrillo colonial',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/ladrillo_colonial.jpg',
            'pdf_url': 'pdf/ladrillo_colonial.pdf',
            'precio': 1600.00
        },
        {
            'nombre': 'Piedra Laja',
            'descripcion': 'Molde para baldosas con diseño símil piedra laja',
            'categoria': 'Pisos y Zócalos',
            'subcategoria': 'Línea 20x20',
            'imagen_url': 'img/products/piedra_laja.jpg',
            'pdf_url': 'pdf/piedra_laja.pdf',
            'precio': 1700.00
        }
    ]
    
    for producto in productos_correctos:
        c.execute("""
            INSERT INTO productos (nombre, descripcion, categoria, subcategoria, imagen_url, pdf_url, precio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            producto['nombre'],
            producto['descripcion'],
            producto['categoria'],
            producto['subcategoria'],
            producto['imagen_url'],
            producto['pdf_url'],
            producto['precio']
        ))
        print(f"✅ Producto agregado: {producto['nombre']}")
    
    conn.commit()
    
    # Verificar que se insertaron correctamente
    c.execute("SELECT id, nombre, categoria, subcategoria, precio FROM productos")
    productos = c.fetchall()
    
    print(f"\nProductos insertados correctamente ({len(productos)}):")
    for producto in productos:
        print(f"  ID: {producto[0]}, Nombre: {producto[1]}, Categoría: {producto[2]}, Subcategoría: {producto[3]}, Precio: ${producto[4]}")
    
    conn.close()
    print("\n✅ Datos corregidos exitosamente!")

if __name__ == "__main__":
    limpiar_y_corregir_datos()
