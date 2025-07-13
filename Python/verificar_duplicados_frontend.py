import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("🔍 Verificando duplicados en BD...")

# Verificar Deck Símil Madera
c.execute("SELECT id, nombre FROM productos WHERE nombre LIKE '%Deck%Madera%'")
deck_productos = c.fetchall()

print("Productos 'Deck Símil Madera':")
for row in deck_productos:
    print(f"   ID: {row[0]} | {row[1]}")

print()

# Verificar duplicados por ID
c.execute("SELECT id, COUNT(*) FROM productos GROUP BY id HAVING COUNT(*) > 1")
ids_duplicados = c.fetchall()

if ids_duplicados:
    print("⚠️ IDs duplicados:")
    for id_val, count in ids_duplicados:
        print(f"   ID {id_val}: {count} veces")
else:
    print("✅ No hay IDs duplicados")

print()

# Ver producto ID 39 específicamente
c.execute("SELECT * FROM productos WHERE id = 39")
producto_39 = c.fetchall()
print("Producto con ID 39:")
for row in producto_39:
    print(f"   {row}")

conn.close()
