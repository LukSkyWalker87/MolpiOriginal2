import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'python', 'molpi.db')

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

# Eliminar todas las subcategorías actuales asociadas a Insumos
c.execute("DELETE FROM subcategorias WHERE categoria_id = ?", (categoria_id,))

# Insertar las subcategorías nuevas
for nombre in SUBCATEGORIAS_NUEVAS:
    c.execute("INSERT INTO subcategorias (nombre, categoria_id) VALUES (?, ?)", (nombre, categoria_id))

conn.commit()
print("Subcategorías actualizadas en python/molpi.db")
conn.close()
