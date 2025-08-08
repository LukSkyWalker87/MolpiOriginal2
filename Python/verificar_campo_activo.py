import sqlite3
import os
from datetime import datetime

# Ruta a la base de datos
db_path = '../molpi.db'

def verificar_campo_activo():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar la estructura de la tabla productos
        cursor.execute("PRAGMA table_info(productos)")
        columnas = cursor.fetchall()
        
        # Buscar el campo 'activo'
        campo_activo = None
        for columna in columnas:
            if columna[1] == 'activo':
                campo_activo = columna
                break
        
        if campo_activo:
            print(f"✅ El campo 'activo' existe en la tabla productos:")
            print(f"   - Nombre: {campo_activo[1]}")
            print(f"   - Tipo: {campo_activo[2]}")
            print(f"   - ¿Puede ser NULL?: {'Sí' if campo_activo[3] == 0 else 'No'}")
            print(f"   - Valor por defecto: {campo_activo[4]}")
        else:
            print("❌ El campo 'activo' no existe en la tabla productos")
            
        # Contar cuántos productos tienen el campo activo configurado
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
        activos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo = 0")
        inactivos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM productos WHERE activo IS NULL")
        nulos = cursor.fetchone()[0]
        
        total = activos + inactivos + nulos
        
        print(f"\nEstadísticas de productos:")
        print(f"- Total de productos: {total}")
        print(f"- Productos activos: {activos} ({round(activos/total*100 if total > 0 else 0, 2)}%)")
        print(f"- Productos inactivos: {inactivos} ({round(inactivos/total*100 if total > 0 else 0, 2)}%)")
        print(f"- Productos sin estado definido: {nulos} ({round(nulos/total*100 if total > 0 else 0, 2)}%)")
        
        # Mostrar algunos ejemplos de productos con su estado
        print("\nEjemplos de productos:")
        cursor.execute("""
            SELECT id, nombre, categoria, activo 
            FROM productos 
            ORDER BY RANDOM()
            LIMIT 5
        """)
        ejemplos = cursor.fetchall()
        
        for producto in ejemplos:
            estado = "Activo" if producto[3] == 1 else "Inactivo" if producto[3] == 0 else "No definido"
            print(f"- ID: {producto[0]}, Nombre: {producto[1]}, Categoría: {producto[2]}, Estado: {estado}")
        
        # Si hay productos "Green", mostrarlos específicamente
        print("\nProductos de categoría 'Green':")
        cursor.execute("""
            SELECT id, nombre, subcategoria, activo 
            FROM productos 
            WHERE categoria = 'Green'
            ORDER BY nombre
        """)
        green_productos = cursor.fetchall()
        
        if green_productos:
            for producto in green_productos:
                estado = "Activo" if producto[3] == 1 else "Inactivo" if producto[3] == 0 else "No definido"
                print(f"- ID: {producto[0]}, Nombre: {producto[1]}, Subcategoría: {producto[2]}, Estado: {estado}")
        else:
            print("No hay productos en la categoría 'Green'")
        
        conn.close()
        
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")

if __name__ == "__main__":
    print(f"Verificación de campo 'activo' en la tabla productos")
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    verificar_campo_activo()
