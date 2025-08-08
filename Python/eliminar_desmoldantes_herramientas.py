import sqlite3

def eliminar_desmoldantes_y_herramientas():
    """Elimina todos los productos de las subcategorías 'Desmoldantes' y 'Herramientas' en Insumos"""
    
    # Conectar a la base de datos
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    try:
        # Primero mostrar qué productos vamos a eliminar
        print("Productos que serán eliminados:")
        cursor.execute('''
            SELECT id, nombre, descripcion, subcategoria
            FROM productos 
            WHERE categoria = "Insumos" AND subcategoria IN ("Desmoldantes", "Herramientas")
        ''')
        productos = cursor.fetchall()
        
        if not productos:
            print("No se encontraron productos en las subcategorías 'Desmoldantes' y 'Herramientas'")
            return
        
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Subcategoría: {producto[3]}")
        
        # Confirmar eliminación
        print(f"\nSe eliminarán {len(productos)} productos.")
        
        # Eliminar los productos
        cursor.execute('''
            DELETE FROM productos 
            WHERE categoria = "Insumos" AND subcategoria IN ("Desmoldantes", "Herramientas")
        ''')
        
        # Confirmar cambios
        conn.commit()
        print(f"✅ Se eliminaron {cursor.rowcount} productos de las subcategorías 'Desmoldantes' y 'Herramientas'")
        
        # Verificar que se eliminaron
        cursor.execute('''
            SELECT COUNT(*) 
            FROM productos 
            WHERE categoria = "Insumos" AND subcategoria IN ("Desmoldantes", "Herramientas")
        ''')
        count = cursor.fetchone()[0]
        print(f"Productos restantes en 'Desmoldantes' y 'Herramientas': {count}")
        
        # Mostrar subcategorías restantes en Insumos
        print("\nSubcategorías restantes en Insumos:")
        cursor.execute('''
            SELECT subcategoria, COUNT(*) as total
            FROM productos 
            WHERE categoria = "Insumos" AND activo = 1
            GROUP BY subcategoria
            ORDER BY subcategoria
        ''')
        subcategorias = cursor.fetchall()
        for sub, total in subcategorias:
            print(f"  {sub}: {total} productos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    eliminar_desmoldantes_y_herramientas()
