import sqlite3

def corregir_imagen_laja_20x40_final():
    try:
        conn = sqlite3.connect('molpi.db')
        cursor = conn.cursor()
        
        # Actualizar con la imagen correcta que existe
        nueva_imagen = "img/products/laja_n2_40x20_molde.jpg"
        cursor.execute("UPDATE productos SET imagen_url = ? WHERE nombre LIKE '%Laja 20x40%'", 
                     (nueva_imagen,))
        
        conn.commit()
        print(f"✓ Imagen actualizada para Laja 20x40: {nueva_imagen}")
        
        # Verificar el cambio
        cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE nombre LIKE '%Laja 20x40%'")
        resultado = cursor.fetchone()
        print(f"Verificación: ID {resultado[0]} - {resultado[1]} - {resultado[2]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    corregir_imagen_laja_20x40_final()
