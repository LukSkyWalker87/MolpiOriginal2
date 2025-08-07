#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def limpiar_productos_50x50():
    """
    Elimina los productos sobrantes de la línea 50x50, dejando solo los 8 correctos
    """
    
    db_path = "molpi.db"
    
    # IDs de productos que deben SER ELIMINADOS
    productos_a_eliminar = [
        33,  # Lisa 50x50 (duplicado, ya tenemos "Liso" ID 103)
        34,  # Gregoriana 50x50 (no está en las imágenes)
        35,  # Corteza 50x50 (duplicado, ya tenemos "Corteza" ID 105)
    ]
    
    # Productos que deben QUEDARSE (según las imágenes):
    productos_correctos = {
        98: "Laja San Juan",
        99: "Adoquín Colonial", 
        100: "Deck Símil Madera",
        101: "Deck Antideslizante",
        102: "Madera 50x25x6 / 2 piezas por molde",
        103: "Liso",
        104: "Quebracho", 
        105: "Corteza"
    }
    
    print("=== LIMPIEZA DE PRODUCTOS LÍNEA 50x50 ===\n")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Mostrar productos antes de la eliminación
        print("📋 PRODUCTOS ANTES DE LA LIMPIEZA:")
        cursor.execute("SELECT id, nombre FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
        productos_antes = cursor.fetchall()
        
        for id_prod, nombre in productos_antes:
            print(f"ID: {id_prod:3d} | {nombre}")
        
        print(f"\nTotal antes: {len(productos_antes)} productos")
        print("="*60)
        
        # Eliminar productos sobrantes
        productos_eliminados = 0
        
        for id_producto in productos_a_eliminar:
            # Obtener información del producto antes de eliminarlo
            cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
            resultado = cursor.fetchone()
            
            if resultado:
                nombre_producto = resultado[0]
                
                # Eliminar el producto
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                
                print(f"🗑️  ELIMINADO ID {id_producto}: {nombre_producto}")
                productos_eliminados += 1
            else:
                print(f"⚠️  Producto ID {id_producto} no encontrado")
        
        # Confirmar cambios
        conn.commit()
        
        print(f"\n✅ ELIMINACIÓN COMPLETADA: {productos_eliminados} productos eliminados")
        print("="*60)
        
        # Mostrar productos después de la limpieza
        print("\n📋 PRODUCTOS DESPUÉS DE LA LIMPIEZA:")
        cursor.execute("SELECT id, nombre, imagen_url FROM productos WHERE subcategoria = 'Línea 50x50' ORDER BY id")
        productos_despues = cursor.fetchall()
        
        for id_prod, nombre, imagen_url in productos_despues:
            print(f"ID: {id_prod:3d} | {nombre:40s} | {imagen_url}")
        
        print(f"\nTotal después: {len(productos_despues)} productos")
        
        # Verificar que tengamos exactamente 8 productos
        if len(productos_despues) == 8:
            print("\n🎉 ¡PERFECTO! Ahora tienes exactamente 8 productos en la línea 50x50")
        else:
            print(f"\n⚠️  Advertencia: Se esperaban 8 productos, pero hay {len(productos_despues)}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    limpiar_productos_50x50()
