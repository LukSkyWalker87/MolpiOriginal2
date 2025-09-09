import sqlite3
import os

# Ruta a la base de datos (ajusta según tu entorno de producción)
DB_PATH = 'backend/molpi.db'

# Carpeta donde deberían estar las imágenes (ajusta si es necesario)
IMG_DIR = 'www.molpi.com.ar/img/products/'

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print(f"{'ID':<5} {'Nombre':<40} {'imagen_url':<40} {'¿Existe?'}")
print('-'*100)

for row in c.execute("SELECT id, nombre, imagen_url FROM productos ORDER BY id DESC LIMIT 30"):
    id_, nombre, imagen_url = row
    if not imagen_url:
        existe = 'NO URL'
    else:
        # Quitar barra inicial si la tiene
        img_path = imagen_url.lstrip('/')
        full_path = os.path.join(IMG_DIR, os.path.basename(img_path))
        existe = 'SI' if os.path.exists(full_path) else 'NO'
    print(f"{id_:<5} {nombre[:38]:<40} {str(imagen_url)[:38]:<40} {existe}")

conn.close()
