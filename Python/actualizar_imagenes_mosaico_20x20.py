#!/usr/bin/env python3
"""Script para agregar imágenes de mosaico a productos existentes de la línea 20x20"""

import sqlite3
import os

def actualizar_imagenes_mosaico():
    """Agregar URLs de imágenes de mosaico a productos específicos de la línea 20x20"""
    
    db_path = 'molpi.db'
    if not os.path.exists(db_path):
        print(f"❌ Error: No se encontró la base de datos {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Mapeo de productos y sus imágenes de mosaico correspondientes
        actualizaciones = [
            {
                'nombre_buscar': 'Vainilla de 3',
                'imagen_mosaico': 'img/products/vainilla_de_3_mosaico.png'
            },
            {
                'nombre_buscar': 'Vainilla de 6',
                'imagen_mosaico': 'img/products/vainilla_de_6_mosaico.png'
            },
            {
                'nombre_buscar': 'Lisa 20x20',
                'imagen_mosaico': 'img/products/lisa_20_mosaico.png'
            },
            {
                'nombre_buscar': 'Liso 20x20',
                'imagen_mosaico': 'img/products/lisa_20_mosaico_b.png'
            }
        ]
        
        print("🔍 Buscando productos de la línea 20x20...")
        
        # Mostrar productos actuales de la línea 20x20
        c.execute("""
            SELECT id, nombre, imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20'
            ORDER BY nombre
        """)
        productos_actuales = c.fetchall()
        
        print(f"📋 Productos encontrados en línea 20x20: {len(productos_actuales)}")
        for producto in productos_actuales:
            print(f"  - ID: {producto[0]} | Nombre: {producto[1]} | Mosaico: {producto[3] or 'Sin mosaico'}")
        
        # Realizar actualizaciones
        actualizaciones_realizadas = 0
        
        for actualizacion in actualizaciones:
            nombre_buscar = actualizacion['nombre_buscar']
            imagen_mosaico = actualizacion['imagen_mosaico']
            
            # Buscar producto que contenga el nombre (búsqueda flexible)
            c.execute("""
                UPDATE productos 
                SET imagen_mosaico_url = ?
                WHERE activo = 1 
                AND categoria = 'Pisos y Zócalos' 
                AND subcategoria = 'Línea 20x20'
                AND nombre LIKE ?
            """, (imagen_mosaico, f'%{nombre_buscar}%'))
            
            if c.rowcount > 0:
                print(f"✅ Actualizado: {nombre_buscar} -> {imagen_mosaico}")
                actualizaciones_realizadas += 1
            else:
                print(f"⚠️  No se encontró producto que contenga: {nombre_buscar}")
        
        conn.commit()
        conn.close()
        
        print(f"\n🎉 Proceso completado: {actualizaciones_realizadas} productos actualizados")
        
        # Mostrar estado final
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            SELECT id, nombre, imagen_url, imagen_mosaico_url 
            FROM productos 
            WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20'
            ORDER BY nombre
        """)
        productos_finales = c.fetchall()
        conn.close()
        
        print("\n📋 Estado final de productos 20x20:")
        for producto in productos_finales:
            estado_mosaico = "✅ Con mosaico" if producto[3] else "⚪ Sin mosaico"
            print(f"  - {producto[1]} | {estado_mosaico}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Actualizando imágenes de mosaico para línea 20x20 ===")
    success = actualizar_imagenes_mosaico()
    if success:
        print("\n🎯 ¡Actualización completada exitosamente!")
        print("💡 Los productos ahora tienen imágenes de mosaico configuradas")
    else:
        print("\n💥 El proceso falló")
