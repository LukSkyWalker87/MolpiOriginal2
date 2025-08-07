#!/usr/bin/env python3
import sqlite3

# Limpiar productos podotáctiles duplicados/inactivos
DB_PATH = 'Python/molpi.db'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Eliminar físicamente los productos inactivos que están duplicados
productos_a_eliminar = [106, 107, 109, 111, 112]

print("🧹 Limpiando productos podotáctiles duplicados...")

for producto_id in productos_a_eliminar:
    c.execute("DELETE FROM productos WHERE id = ? AND activo = 0", (producto_id,))
    print(f"   Eliminado producto ID {producto_id}")

conn.commit()

# Verificar productos podotáctiles restantes
c.execute("SELECT id, nombre, activo FROM productos WHERE categoria = 'Podotáctiles' ORDER BY id")
productos = c.fetchall()

print("\n✅ Productos podotáctiles finales:")
for producto in productos:
    status = "ACTIVO" if producto[2] == 1 else "INACTIVO"
    print(f"   ID {producto[0]}: {producto[1]} - {status}")

conn.close()
print("\n🎉 Limpieza completada!")
