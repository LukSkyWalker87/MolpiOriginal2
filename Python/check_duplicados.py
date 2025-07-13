import sqlite3

print("🔍 Verificación rápida de duplicados...")

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Contar total
c.execute("SELECT COUNT(*) FROM productos")
total = c.fetchone()[0]
print(f"Total productos en BD: {total}")

# Buscar duplicados por nombre
c.execute("""
    SELECT nombre, COUNT(*) 
    FROM productos 
    GROUP BY nombre 
    HAVING COUNT(*) > 1
""")
duplicados = c.fetchall()

if duplicados:
    print(f"⚠️ {len(duplicados)} productos con nombres duplicados:")
    for nombre, count in duplicados:
        print(f"  '{nombre}': {count} copias")
else:
    print("✅ No hay productos duplicados")

# Buscar duplicados por ID
c.execute("""
    SELECT id, COUNT(*) 
    FROM productos 
    GROUP BY id 
    HAVING COUNT(*) > 1
""")
ids_duplicados = c.fetchall()

if ids_duplicados:
    print(f"⚠️ {len(ids_duplicados)} IDs duplicados")
else:
    print("✅ No hay IDs duplicados")

conn.close()
