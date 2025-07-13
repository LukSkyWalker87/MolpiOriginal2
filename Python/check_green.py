import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("🔍 Verificando productos por categoría...")
c.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria ORDER BY categoria")
for cat, count in c.fetchall():
    print(f"{cat}: {count} productos")

print()
print("🌱 Productos de Green:")
c.execute("SELECT id, nombre, categoria FROM productos WHERE categoria = 'Green'")
for row in c.fetchall():
    print(f"  ID {row[0]}: {row[1]} ({row[2]})")

conn.close()
