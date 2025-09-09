import sqlite3


# Ruta correcta a la base de datos usada por el proyecto
import os
DB_PATH = os.path.join(os.path.dirname(__file__), 'python', 'molpi.db')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


# Eliminar subcategoría 'Pigmentos' solo de la categoría 'Insumos'
c.execute("""
    DELETE FROM subcategorias 
    WHERE nombre = ? AND categoria_id = (
        SELECT id FROM categorias WHERE nombre = ?
    )
""", ("Pigmentos", "Insumos"))

conn.commit()
print("Subcategoría 'Pigmentos' eliminada de 'Insumos'.")
conn.close()
