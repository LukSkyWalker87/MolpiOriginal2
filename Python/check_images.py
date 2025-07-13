import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("🔍 Verificando imágenes en la base de datos...")
c.execute("SELECT id, nombre, imagen_url FROM productos LIMIT 10")
for row in c.fetchall():
    print(f"ID {row[0]}: {row[1]} -> {row[2]}")

conn.close()
