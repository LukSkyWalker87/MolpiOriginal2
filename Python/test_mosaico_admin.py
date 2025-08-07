#!/usr/bin/env python3
"""Script de prueba para verificar funcionamiento de mosaicos en admin"""

import sqlite3
import os

def test_mosaico_admin():
    """Verificar que un producto específico tenga mosaico para probar en admin"""
    
    db_path = 'molpi.db'
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Buscar productos con mosaico en línea 20x20
        c.execute("""
            SELECT id, nombre, imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE activo = 1 
            AND categoria = 'Pisos y Zócalos' 
            AND subcategoria = 'Línea 20x20'
            AND imagen_mosaico_url IS NOT NULL 
            AND imagen_mosaico_url != ''
            ORDER BY id
        """)
        
        productos_con_mosaico = c.fetchall()
        
        print("🔍 Productos con mosaico configurado:")
        print("-" * 60)
        
        for producto in productos_con_mosaico:
            id_prod, nombre, imagen_molde, imagen_mosaico = producto
            print(f"ID: {id_prod:2d} | {nombre:20s}")
            print(f"     Molde:   {imagen_molde}")
            print(f"     Mosaico: {imagen_mosaico}")
            print()
        
        # Si no hay productos con mosaico, agregar uno para prueba
        if not productos_con_mosaico:
            print("⚠️  No hay productos con mosaico. Agregando uno para prueba...")
            
            # Buscar el primer producto de línea 20x20
            c.execute("""
                SELECT id, nombre FROM productos 
                WHERE activo = 1 
                AND categoria = 'Pisos y Zócalos' 
                AND subcategoria = 'Línea 20x20'
                LIMIT 1
            """)
            
            primer_producto = c.fetchone()
            
            if primer_producto:
                producto_id, nombre = primer_producto
                imagen_mosaico = 'img/products/vainilla_de_3_mosaico.png'
                
                c.execute("""
                    UPDATE productos 
                    SET imagen_mosaico_url = ?
                    WHERE id = ?
                """, (imagen_mosaico, producto_id))
                
                conn.commit()
                print(f"✅ Agregado mosaico a '{nombre}' (ID: {producto_id})")
                print(f"   Imagen mosaico: {imagen_mosaico}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Verificación de Mosaicos para Admin ===")
    success = test_mosaico_admin()
    if success:
        print("\n🎯 ¡Listo para probar en admin!")
        print("💡 Ve al admin, filtra por Línea 20x20 y edita un producto con mosaico")
    else:
        print("\n💥 Error en la verificación")
