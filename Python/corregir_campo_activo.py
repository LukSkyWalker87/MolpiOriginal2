import sqlite3
import os
from datetime import datetime

# Ruta a la base de datos
db_path = '../molpi.db'

def verificar_y_corregir_campo_activo():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Verificando el campo 'activo' en la tabla productos...")
        
        # Verificar si hay productos sin el campo activo definido
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo IS NULL")
        nulos = cursor.fetchone()[0]
        
        if nulos > 0:
            print(f"⚠️ Se encontraron {nulos} productos sin estado definido.")
            
            # Actualizar productos sin estado definido a activo por defecto
            cursor.execute("UPDATE productos SET activo = 1 WHERE activo IS NULL")
            conn.commit()
            print(f"✅ Se actualizaron {nulos} productos a estado 'Activo'.")
        else:
            print("✅ Todos los productos tienen un estado definido.")
        
        # Verificar específicamente los productos de la categoría Green
        cursor.execute("SELECT id, nombre, activo FROM productos WHERE categoria = 'Green'")
        productos_green = cursor.fetchall()
        
        if productos_green:
            print(f"\nProductos de categoría 'Green' ({len(productos_green)}):")
            for producto in productos_green:
                estado = "Activo" if producto[2] == 1 else "Inactivo" if producto[2] == 0 else "No definido"
                print(f"- ID: {producto[0]}, Nombre: {producto[1]}, Estado: {estado}")
                
                # Si el estado no está definido, actualizar a activo
                if producto[2] is None:
                    cursor.execute("UPDATE productos SET activo = 1 WHERE id = ?", (producto[0],))
                    conn.commit()
                    print(f"  ✅ Se actualizó el estado a 'Activo'.")
        else:
            print("\nNo hay productos en la categoría 'Green'")
        
        # Mostrar un resumen general de estados
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
        activos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 0")
        inactivos = cursor.fetchone()[0]
        
        total = activos + inactivos
        
        print(f"\nResumen general de productos:")
        print(f"- Total de productos: {total}")
        print(f"- Productos activos: {activos} ({round(activos/total*100 if total > 0 else 0, 2)}%)")
        print(f"- Productos inactivos: {inactivos} ({round(inactivos/total*100 if total > 0 else 0, 2)}%)")
        
        conn.close()
        print("\nVerificación y corrección completada.")
        
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")

if __name__ == "__main__":
    print(f"Verificación y corrección del campo 'activo' en la tabla productos")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    verificar_y_corregir_campo_activo()
