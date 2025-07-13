import sqlite3

print("🧹 Limpiando productos duplicados...")

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# 1. Primero ver el problema
print("\n📊 Antes de la limpieza:")
c.execute("SELECT COUNT(*) FROM productos")
total_antes = c.fetchone()[0]
print(f"   Total productos: {total_antes}")

# Ver duplicados específicos
c.execute("""
    SELECT nombre, COUNT(*) as cantidad 
    FROM productos 
    GROUP BY nombre 
    HAVING COUNT(*) > 1 
    ORDER BY cantidad DESC 
    LIMIT 10
""")
duplicados = c.fetchall()
print(f"   Productos duplicados: {len(duplicados)}")
for nombre, cantidad in duplicados:
    print(f"   • '{nombre}': {cantidad} copias")

# 2. Eliminar duplicados manteniendo solo el registro con ID más bajo
print("\n🗑️ Eliminando duplicados...")
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

# 3. Confirmar cambios
conn.commit()

# 4. Verificar resultado
print("\n📊 Después de la limpieza:")
c.execute("SELECT COUNT(*) FROM productos")
total_despues = c.fetchone()[0]
print(f"   Total productos: {total_despues}")

# Mostrar resumen por categoría
print("\n📋 Productos únicos por categoría:")
c.execute("""
    SELECT categoria, COUNT(*) 
    FROM productos 
    GROUP BY categoria 
    ORDER BY categoria
""")
for categoria, cantidad in c.fetchall():
    print(f"   • {categoria}: {cantidad} productos")

# 5. Verificar que no hay más duplicados
c.execute("""
    SELECT nombre, COUNT(*) 
    FROM productos 
    GROUP BY nombre 
    HAVING COUNT(*) > 1
""")
duplicados_restantes = c.fetchall()
print(f"\n✅ Duplicados restantes: {len(duplicados_restantes)}")

conn.close()
print("\n🎉 ¡Limpieza completada!")
