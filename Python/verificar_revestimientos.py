import sqlite3

def verificar_revestimientos():
    """Verificar los productos de revestimientos en la base de datos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    try:
        # Mostrar subcategorías
        print("Subcategorías en Revestimientos:")
        cursor.execute('''
            SELECT subcategoria, COUNT(*) as total
            FROM productos 
            WHERE categoria = "Revestimientos" AND activo = 1
            GROUP BY subcategoria
            ORDER BY subcategoria
        ''')
        subcategorias = cursor.fetchall()
        for sub, total in subcategorias:
            print(f"  {sub}: {total} productos")
        
        print("\nTodos los productos de Revestimientos:")
        cursor.execute('''
            SELECT nombre, subcategoria, descripcion
            FROM productos 
            WHERE categoria = "Revestimientos" AND activo = 1
            ORDER BY subcategoria, nombre
        ''')
        productos = cursor.fetchall()
        for nombre, sub, desc in productos:
            print(f"  {sub}: {nombre} - {desc}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_revestimientos()
