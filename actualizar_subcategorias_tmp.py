import sqlite3

DB_PATH = r'C:\tmp\molpi.db'

SUBCATEGORIAS_NUEVAS = [
    'Curadores',
    'Pigmentos Básicos',
    'Pigmentos Concentrados',
    'Pigmentos Extra',
    'Materiales',
    'Desmoldantes',
    'Herramientas',
]

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Obtener el id de la categoría Insumos
c.execute("SELECT id FROM categorias WHERE nombre = 'Insumos'")
row = c.fetchone()
if not row:
    print("No existe la categoría 'Insumos'")
    conn.close()
    exit(1)
categoria_id = row[0]

# Eliminar todas las subcategorías 'Pigmentos' asociadas a Insumos
c.execute("DELETE FROM subcategorias WHERE nombre = 'Pigmentos' AND categoria_id = ?", (categoria_id,))

# Eliminar duplicados de las subcategorías nuevas antes de insertar
for nombre in SUBCATEGORIAS_NUEVAS:
    c.execute("DELETE FROM subcategorias WHERE nombre = ? AND categoria_id = ?", (nombre, categoria_id))
    c.execute("INSERT INTO subcategorias (nombre, categoria_id) VALUES (?, ?)", (nombre, categoria_id))

conn.commit()
print("Subcategorías actualizadas en C:/tmp/molpi.db")
conn.close()
