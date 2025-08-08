import sqlite3

def corregir_revestimientos():
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    print("=== CORRIGIENDO PRODUCTOS DE REVESTIMIENTOS ===")
    
    # Corregir el producto 3D que está mal clasificado
    cursor.execute("""
        UPDATE productos 
        SET subcategoria = '3D', 
            imagen_url = 'img/products/3d_molde.jpg',
            imagen_mosaico_url = 'img/products/revestimiento_3dgris_mosaico.png',
            descripcion = '3 piezas de 35x11,5cm'
        WHERE nombre = '3D Relieve' AND categoria = 'Revestimientos'
    """)
    
    # Eliminar el producto 3D duplicado en Geometricos
    cursor.execute("""
        DELETE FROM productos 
        WHERE nombre = '3D' AND subcategoria = 'Geometricos' AND categoria = 'Revestimientos'
    """)
    
    # Corregir URLs de imágenes mosaico que tienen .html en lugar de .png
    cursor.execute("""
        UPDATE productos 
        SET imagen_mosaico_url = NULL
        WHERE nombre = 'Símil Piedra' AND categoria = 'Revestimientos'
    """)
    
    cursor.execute("""
        UPDATE productos 
        SET imagen_mosaico_url = NULL
        WHERE nombre = 'Laja 20x40' AND categoria = 'Revestimientos'
    """)
    
    cursor.execute("""
        UPDATE productos 
        SET imagen_mosaico_url = NULL
        WHERE nombre = 'Revestimiento 20x40' AND categoria = 'Revestimientos'
    """)
    
    conn.commit()
    
    print("=== VERIFICANDO CORRECCIONES ===")
    
    cursor.execute("""
        SELECT nombre, subcategoria, imagen_url, imagen_mosaico_url, descripcion
        FROM productos 
        WHERE categoria = 'Revestimientos'
        ORDER BY subcategoria, nombre
    """)
    
    productos = cursor.fetchall()
    
    for producto in productos:
        nombre, subcategoria, imagen_url, imagen_mosaico_url, descripcion = producto
        print(f"\nNombre: {nombre}")
        print(f"Subcategoría: {subcategoria}")
        print(f"Imagen molde: {imagen_url}")
        print(f"Imagen mosaico: {imagen_mosaico_url}")
        print(f"Descripción: {descripcion}")
        print("-" * 50)
    
    conn.close()
    print("✅ Correcciones aplicadas exitosamente")

if __name__ == "__main__":
    corregir_revestimientos()
