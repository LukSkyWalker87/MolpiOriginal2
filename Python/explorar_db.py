import sqlite3
import json

def explorar_base_datos():
    print("="*60)
    print("           EXPLORADOR DE BASE DE DATOS MOLPI")
    print("="*60)
    
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    # Mostrar todas las tablas
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = [tabla[0] for tabla in c.fetchall()]
    print(f"\n📊 TABLAS ENCONTRADAS ({len(tablas)}):")
    for i, tabla in enumerate(tablas, 1):
        print(f"  {i}. {tabla}")
    
    # Mostrar productos
    print(f"\n📦 PRODUCTOS:")
    c.execute("SELECT id, nombre, categoria, subcategoria, precio FROM productos WHERE activo = 1")
    productos = c.fetchall()
    
    if productos:
        for producto in productos:
            print(f"  🔹 ID: {producto[0]:2d} | {producto[1]:20s} | {producto[2]:15s} | {producto[3]:12s} | ${producto[4]:6.2f}")
    else:
        print("  ❌ No hay productos activos")
    
    # Mostrar categorías
    print(f"\n🏷️  CATEGORÍAS:")
    c.execute("SELECT id, nombre, descripcion FROM categorias WHERE activo = 1")
    categorias = c.fetchall()
    
    for categoria in categorias:
        print(f"  🔹 {categoria[0]}. {categoria[1]}")
        
        # Subcategorías de esta categoría
        c.execute("SELECT nombre FROM subcategorias WHERE categoria_id = ? AND activo = 1", (categoria[0],))
        subcategorias = c.fetchall()
        for sub in subcategorias:
            print(f"     └── {sub[0]}")
    
    # Estadísticas
    print(f"\n📈 ESTADÍSTICAS:")
    c.execute("SELECT COUNT(*) FROM productos WHERE activo = 1")
    total_productos = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM categorias WHERE activo = 1")
    total_categorias = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM subcategorias WHERE activo = 1")
    total_subcategorias = c.fetchone()[0]
    
    print(f"  📦 Productos activos: {total_productos}")
    print(f"  🏷️  Categorías activas: {total_categorias}")
    print(f"  🔖 Subcategorías activas: {total_subcategorias}")
    
    # Información de la base de datos
    print(f"\n💾 INFORMACIÓN DE LA BASE:")
    import os
    db_path = os.path.abspath('molpi.db')
    db_size = os.path.getsize('molpi.db')
    
    print(f"  📁 Ubicación: {db_path}")
    print(f"  📏 Tamaño: {db_size:,} bytes ({db_size/1024:.1f} KB)")
    
    conn.close()
    
    print(f"\n" + "="*60)
    print("✅ Exploración completada")
    print("="*60)

if __name__ == "__main__":
    explorar_base_datos()
