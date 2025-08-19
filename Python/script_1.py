import os
import shutil

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def mover_archivos(origen, destino, extensiones=None):
    if not os.path.exists(destino):
        os.makedirs(destino)
    for archivo in os.listdir(origen):
        ruta_archivo = os.path.join(origen, archivo)
        if os.path.isfile(ruta_archivo):
            if not extensiones or archivo.lower().endswith(extensiones):
                shutil.copy2(ruta_archivo, os.path.join(destino, archivo))

# Mover HTML
mover_archivos(
    os.path.join(BASE, "www.molpi.com.ar"),
    os.path.join(BASE, "backend", "templates"),
    extensiones=(".html",)
)

# Mover CSS
mover_archivos(
    os.path.join(BASE, "www.molpi.com.ar", "css"),
    os.path.join(BASE, "backend", "static", "css")
)

# Mover JS
mover_archivos(
    os.path.join(BASE, "www.molpi.com.ar", "js"),
    os.path.join(BASE, "backend", "static", "js")
)

# Mover IMG
mover_archivos(
    os.path.join(BASE, "www.molpi.com.ar", "img"),
    os.path.join(BASE, "backend", "static", "img")
)

print("¡Listo! Archivos copiados. Ahora adapta los HTML para usar url_for('static', ...).")