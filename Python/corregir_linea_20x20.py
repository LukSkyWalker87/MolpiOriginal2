import sqlite3
from datetime import datetime

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Fecha actual
fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print("=== AGREGANDO PRODUCTOS FALTANTES ===")

# 1. Vainilla de 3
c.execute("""
INSERT INTO productos (nombre, descripcion, categoria, subcategoria, activo, fecha_creacion, fecha_modificacion)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    'Vainilla de 3',
    'Molde para baldosas con diseño vainilla de 3 cm',
    'Pisos y Zócalos',
    'Línea 20x20',
    1,
    fecha_actual,
    fecha_actual
))

# 2. Vainilla de 4
c.execute("""
INSERT INTO productos (nombre, descripcion, categoria, subcategoria, activo, fecha_creacion, fecha_modificacion)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    'Vainilla de 4',
    'Molde para baldosas con diseño vainilla de 4 cm',
    'Pisos y Zócalos',
    'Línea 20x20',
    1,
    fecha_actual,
    fecha_actual
))

# 3. 9 Panes
c.execute("""
INSERT INTO productos (nombre, descripcion, categoria, subcategoria, activo, fecha_creacion, fecha_modificacion)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    '9 Panes',
    'Molde para baldosas con diseño de 9 panes',
    'Pisos y Zócalos',
    'Línea 20x20',
    1,
    fecha_actual,
    fecha_actual
))

# 4. Laja 20x20
c.execute("""
INSERT INTO productos (nombre, descripcion, categoria, subcategoria, activo, fecha_creacion, fecha_modificacion)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    'Laja 20x20',
    'Molde para baldosas con diseño laja 20x20',
    'Pisos y Zócalos',
    'Línea 20x20',
    1,
    fecha_actual,
    fecha_actual
))

# 5. Liso 20x20
c.execute("""
INSERT INTO productos (nombre, descripcion, categoria, subcategoria, activo, fecha_creacion, fecha_modificacion)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    'Liso 20x20',
    'Molde para baldosas lisas 20x20',
    'Pisos y Zócalos',
    'Línea 20x20',
    1,
    fecha_actual,
    fecha_actual
))

print("Productos agregados exitosamente")

print("\n=== MOVIENDO PRODUCTOS INCORRECTOS A OTRAS CATEGORÍAS ===")

# Mover productos que no corresponden a línea 20x20
productos_a_mover = [
    (7, 'Adoquín Rústico', 'Línea 40x40'),
    (8, 'Piedra París', 'Línea 40x40'), 
    (9, 'Ladrillo Colonial', 'Línea 40x40'),
    (36, 'Abanico Liso', 'Línea 40x40'),
    (37, 'Abanico Rústico', 'Línea 40x40'),
    (38, 'Flor Circular', 'Línea 40x40'),
    (39, 'Deck Símil Madera', 'Línea 40x40')
]

for producto_id, nombre, nueva_subcategoria in productos_a_mover:
    c.execute("""
    UPDATE productos 
    SET subcategoria = ?, fecha_modificacion = ?
    WHERE id = ?
    """, (nueva_subcategoria, fecha_actual, producto_id))
    print(f"Movido: {nombre} -> {nueva_subcategoria}")

# También podemos mover Laja 20x40 a línea 20x20 si corresponde
c.execute("""
UPDATE productos 
SET categoria = 'Pisos y Zócalos', subcategoria = 'Línea 20x20', fecha_modificacion = ?
WHERE id = 23 AND nombre = 'Laja 20x40'
""", (fecha_actual,))
print("Movido: Laja 20x40 -> Línea 20x20")

conn.commit()

print("\n=== VERIFICANDO RESULTADO FINAL ===")
c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20' ORDER BY nombre")
productos_finales = c.fetchall()
for p in productos_finales:
    print(f"ID {p[0]}: {p[1]}")

conn.close()
print("\n¡Corrección completada!")
