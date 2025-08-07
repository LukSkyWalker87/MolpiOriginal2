import sqlite3

conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Verificar estructura actual de la tabla productos
cursor.execute("PRAGMA table_info(productos)")
columnas = cursor.fetchall()

print("Estructura actual de la tabla productos:")
for col in columnas:
    print(f"  {col[1]} ({col[2]}) - {col[5]}")

conn.close()
