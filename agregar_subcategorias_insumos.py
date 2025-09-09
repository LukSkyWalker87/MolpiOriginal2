import sqlite3

# Subcategorías a agregar
subcategorias = [
    'Curadores',
    'Pigmentos Básicos',
    'Pigmentos Concentrados',
    'Pigmentos Extra',
    'Materiales',
    'Desmoldantes',
    'Herramientas'
]

# Nombre de la categoría principal para insumos (ajustar si es diferente en tu base)
CATEGORIA_NOMBRE = 'Insumos'

conn = sqlite3.connect('backend/molpi.db')
c = conn.cursor()

# Obtener el id de la categoría principal
c.execute("SELECT id FROM categorias WHERE nombre = ?", (CATEGORIA_NOMBRE,))
row = c.fetchone()
if not row:
    raise Exception(f"No existe la categoría '{CATEGORIA_NOMBRE}' en la tabla categorias.")
categoria_id = row[0]

# Insertar subcategorías si no existen
for nombre in subcategorias:
    c.execute("SELECT id FROM subcategorias WHERE nombre = ? AND categoria_id = ?", (nombre, categoria_id))
    if not c.fetchone():
        c.execute("INSERT INTO subcategorias (nombre, categoria_id) VALUES (?, ?)", (nombre, categoria_id))
        print(f"Subcategoría agregada: {nombre}")
    else:
        print(f"Ya existe la subcategoría: {nombre}")

conn.commit()
conn.close()
print("Listo. Subcategorías procesadas.")
