import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("🔍 Estado actual de la base de datos:")
print()

# Verificar productos con 'Laja' en el nombre
c.execute("SELECT id, nombre, categoria, subcategoria, precio FROM productos WHERE nombre LIKE '%Laja%'")
productos_laja = c.fetchall()

if productos_laja:
    print("Productos con 'Laja':")
    for row in productos_laja:
        print(f"   ID: {row[0]} | {row[1]} | {row[2]} | {row[3]} | ${row[4]}")
else:
    print("No se encontraron productos con 'Laja'")

print()

# Mostrar primeros 10 productos
print("Primeros 10 productos:")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos ORDER BY id LIMIT 10")
for row in c.fetchall():
    print(f"   ID: {row[0]} | {row[1]} | {row[2]} | {row[3]}")

print()

# Contar por categoría
print("Resumen por categoría:")
c.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria ORDER BY categoria")
for categoria, count in c.fetchall():
    print(f"   • {categoria}: {count} productos")

conn.close()
