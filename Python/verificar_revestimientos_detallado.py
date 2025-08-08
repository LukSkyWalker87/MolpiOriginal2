import sqlite3

def verificar_revestimientos():
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    print("=== PRODUCTOS DE REVESTIMIENTOS EN BASE DE DATOS ===")
    
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

if __name__ == "__main__":
    verificar_revestimientos()
