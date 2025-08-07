import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("=== PRODUCTOS ACTUALES EN LÍNEA 20x20 ===")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20' ORDER BY id")
productos_20x20 = c.fetchall()
for p in productos_20x20:
    print(f"ID {p[0]}: {p[1]} - {p[2]} / {p[3]}")

print("\n=== TODOS LOS PRODUCTOS CON 'VAINILLA' EN EL NOMBRE ===")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE nombre LIKE '%vainilla%' OR nombre LIKE '%Vainilla%' ORDER BY id")
vainillas = c.fetchall()
for p in vainillas:
    print(f"ID {p[0]}: {p[1]} - {p[2]} / {p[3]}")

print("\n=== PRODUCTOS CON 'PANES' EN EL NOMBRE ===")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE nombre LIKE '%panes%' OR nombre LIKE '%Panes%' ORDER BY id")
panes = c.fetchall()
for p in panes:
    print(f"ID {p[0]}: {p[1]} - {p[2]} / {p[3]}")

print("\n=== PRODUCTOS CON 'LAJA' O 'LISO' EN EL NOMBRE ===")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE nombre LIKE '%laja%' OR nombre LIKE '%Laja%' OR nombre LIKE '%liso%' OR nombre LIKE '%Liso%' ORDER BY id")
laja_liso = c.fetchall()
for p in laja_liso:
    print(f"ID {p[0]}: {p[1]} - {p[2]} / {p[3]}")

conn.close()
