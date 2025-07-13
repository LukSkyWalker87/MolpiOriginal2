import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Verificar qué tablas existen
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = c.fetchall()
print("Tablas en la base de datos:")
for tabla in tablas:
    print(f"  - {tabla[0]}")

print("\n" + "="*50)

# Verificar la estructura de cada tabla
for tabla in tablas:
    tabla_nombre = tabla[0]
    print(f"\nEstructura de la tabla {tabla_nombre}:")
    c.execute(f"PRAGMA table_info({tabla_nombre})")
    columns = c.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Contar registros
    c.execute(f"SELECT COUNT(*) FROM {tabla_nombre}")
    count = c.fetchone()[0]
    print(f"  Registros: {count}")

conn.close()
