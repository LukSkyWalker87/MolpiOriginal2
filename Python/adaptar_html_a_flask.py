import os
import re

TEMPLATES_DIR = os.path.join("backend", "templates")

# Reglas de reemplazo: (regex, reemplazo)
REGLAS = [
    # CSS
    (r'href="css/([^"]+)"', r'href="{{ url_for(\'static\', filename=\'css/\1\') }}"'),
    # JS
    (r'src="js/([^"]+)"', r'src="{{ url_for(\'static\', filename=\'js/\1\') }}"'),
    # IMG
    (r'src="img/([^"]+)"', r'src="{{ url_for(\'static\', filename=\'img/\1\') }}"'),
    (r'href="img/([^"]+)"', r'href="{{ url_for(\'static\', filename=\'img/\1\') }}"'),
    # Favicon
    (r'href="favicon.ico"', r'href="{{ url_for(\'static\', filename=\'img/favicon.ico\') }}"'),
    # Otros recursos (puedes agregar más reglas si tienes otras carpetas)
]

for archivo in os.listdir(TEMPLATES_DIR):
    if archivo.endswith(".html"):
        ruta = os.path.join(TEMPLATES_DIR, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        for patron, reemplazo in REGLAS:
            contenido = re.sub(patron, reemplazo, contenido)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"Adaptado: {archivo}")

print("¡Listo! Los HTML ahora usan url_for('static', ...).")