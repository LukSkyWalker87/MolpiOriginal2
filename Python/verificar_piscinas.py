import sqlite3

def verificar_piscinas():
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    print("=== PRODUCTOS DE PISCINAS EN BASE DE DATOS ===")
    
    cursor.execute("""
        SELECT nombre, subcategoria, imagen_url, imagen_mosaico_url, descripcion
        FROM productos 
        WHERE categoria = 'Piscinas'
        ORDER BY subcategoria, nombre
    """)
    
    productos = cursor.fetchall()
    
    if productos:
        for producto in productos:
            nombre, subcategoria, imagen_url, imagen_mosaico_url, descripcion = producto
            print(f"\nNombre: {nombre}")
            print(f"Subcategoría: {subcategoria}")
            print(f"Imagen molde: {imagen_url}")
            print(f"Imagen mosaico: {imagen_mosaico_url}")
            print(f"Descripción: {descripcion}")
            print("-" * 50)
    else:
        print("No se encontraron productos en la categoría Piscinas")
    
    # Verificar si existe endpoint para piscinas
    print("\n=== VERIFICANDO ESTRUCTURA DE CATEGORÍAS ===")
    cursor.execute("SELECT DISTINCT categoria FROM productos ORDER BY categoria")
    categorias = cursor.fetchall()
    
    print("Categorías disponibles:")
    for cat in categorias:
        print(f"- {cat[0]}")
    
    conn.close()

if __name__ == "__main__":
    verificar_piscinas()
