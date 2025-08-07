import sqlite3

conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

try:
    # Agregar nueva columna precio_usd
    cursor.execute("ALTER TABLE productos ADD COLUMN precio_usd REAL DEFAULT 0")
    print("✅ Columna 'precio_usd' agregada exitosamente")
    
    # Verificar que se agregó correctamente
    cursor.execute("PRAGMA table_info(productos)")
    columnas = cursor.fetchall()
    
    print("\nEstructura actualizada de la tabla productos:")
    for col in columnas:
        print(f"  {col[1]} ({col[2]})")
    
    conn.commit()
    
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("ℹ️ La columna 'precio_usd' ya existe")
    else:
        print(f"❌ Error: {e}")

conn.close()
print("\n🎉 Base de datos actualizada correctamente!")
