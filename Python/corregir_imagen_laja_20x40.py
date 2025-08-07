import sqlite3

def corregir_imagen_laja_20x40():
    try:
        conn = sqlite3.connect('molpi.db')
        cursor = conn.cursor()
        
        # Primero verificar el producto actual
        cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE nombre LIKE '%Laja 20x40%'")
        producto = cursor.fetchone()
        
        if producto:
            print(f"Producto encontrado: ID {producto[0]} - {producto[1]}")
            print(f"Imagen actual: {producto[2]}")
            
            # Actualizar la imagen del producto Laja 20x40
            nueva_imagen = "img/products/Laja 20x40.jpg"
            cursor.execute("UPDATE productos SET imagen_url = ? WHERE id = ?", 
                         (nueva_imagen, producto[0]))
            
            conn.commit()
            print(f"✓ Imagen actualizada para Laja 20x40: {nueva_imagen}")
            
            # Verificar el cambio
            cursor.execute("SELECT nombre, imagen_url FROM productos WHERE id = ?", (producto[0],))
            resultado = cursor.fetchone()
            print(f"Verificación: {resultado[0]} - {resultado[1]}")
            
        else:
            print("❌ No se encontró el producto Laja 20x40")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    corregir_imagen_laja_20x40()
