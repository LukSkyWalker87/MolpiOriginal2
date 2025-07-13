import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("🧹 Limpiando y organizando la base de datos...")

# 1. Limpiar productos duplicados (mantener solo uno por nombre)
print("\n1. Eliminando productos duplicados...")
c.execute("""
    DELETE FROM productos 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM productos 
        GROUP BY nombre
    )
""")
duplicados_eliminados = c.rowcount
print(f"   ✅ {duplicados_eliminados} productos duplicados eliminados")

# 2. Actualizar categorías de productos existentes según su nombre
print("\n2. Asignando categorías correctas...")

categorias_productos = {
    # Pisos y Zócalos
    'Pisos y Zócalos': [
        'Vainilla', 'Lisa', 'Liso', 'Octogonal', 'Riojana', 'Gregoriana',
        'Corteza', 'Quebracho', 'Trapezoide', 'Ondas', 'Barras', 'Círculos',
        'Abanico', 'Flor', 'Ladrillo', 'Piedra', 'Laja', 'Travertino',
        'Madera', 'Deck', '20x20', '40x40', '50x50'
    ],
    # Green (productos ecológicos)
    'Green': [
        'Green', 'Rombo Green', 'Recto Green', 'Círculos Green'
    ],
    # Piscinas
    'Piscinas': [
        'Piscina', 'Arco Romano', 'Borde', 'Ballena', 'Escalón', 'Esquina',
        'Rejilla', 'Travertino 50x50'
    ],
    # Revestimientos
    'Revestimientos': [
        'Revestimiento', '3D', 'Símil Piedra'
    ],
    # Podotáctiles
    'Podotáctiles - Discapacidad': [
        'Discapacitado', 'Podotáctil', 'Antideslizante'
    ],
    # Placas Antihumedad
    'Placas Antihumedad': [
        'Antihumedad', 'Placa'
    ],
    # Insumos
    'Insumos': [
        'Molde', 'Desmoldante', 'Colorante', 'Cemento', 'Arena'
    ]
}

# Actualizar categorías basado en el nombre del producto
for categoria, palabras_clave in categorias_productos.items():
    for palabra in palabras_clave:
        c.execute("""
            UPDATE productos 
            SET categoria = ? 
            WHERE nombre LIKE ? AND categoria != ?
        """, (categoria, f'%{palabra}%', categoria))

# 3. Asignar subcategorías según la categoría
print("\n3. Asignando subcategorías...")

subcategorias_por_categoria = {
    'Pisos y Zócalos': ['Línea 20x20', 'Línea 40x40', 'Línea 50x50'],
    'Green': ['Línea Green'],
    'Piscinas': ['Bordes y Esquinas', 'Escalones', 'Rejillas'],
    'Revestimientos': ['20x40', '3D'],
    'Podotáctiles - Discapacidad': ['Guías', 'Alertas'],
    'Placas Antihumedad': ['Estándar'],
    'Insumos': ['Herramientas', 'Materiales']
}

# Asignar subcategorías por defecto
for categoria, subcategorias in subcategorias_por_categoria.items():
    subcategoria_principal = subcategorias[0]  # Usar la primera como principal
    c.execute("""
        UPDATE productos 
        SET subcategoria = ? 
        WHERE categoria = ? AND (subcategoria IS NULL OR subcategoria = '')
    """, (subcategoria_principal, categoria))

# 4. Limpiar precios (asegurar que sean números válidos)
print("\n4. Limpiando precios...")
c.execute("UPDATE productos SET precio = 0 WHERE precio IS NULL OR precio < 0")

# 5. Asegurar que todos los productos estén activos
print("\n5. Activando todos los productos...")
c.execute("UPDATE productos SET activo = 1")

# Confirmar cambios
conn.commit()

# 6. Mostrar resumen final
print("\n📊 Resumen final:")
c.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria ORDER BY categoria")
resumen = c.fetchall()

print("   Productos por categoría:")
total_productos = 0
for categoria, cantidad in resumen:
    print(f"   • {categoria}: {cantidad} productos")
    total_productos += cantidad

print(f"\n   📦 Total: {total_productos} productos únicos")

# Verificar algunas muestras
print("\n🔍 Muestra de productos organizados:")
c.execute("""
    SELECT nombre, categoria, subcategoria, precio 
    FROM productos 
    ORDER BY categoria, nombre 
    LIMIT 10
""")
muestras = c.fetchall()

for muestra in muestras:
    print(f"   • {muestra[0]} | {muestra[1]} | {muestra[2]} | ${muestra[3]}")

conn.close()
print("\n✅ ¡Base de datos organizada correctamente!")
