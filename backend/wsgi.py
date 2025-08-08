# -*- coding: utf-8 -*-

"""
WSGI config para PythonAnywhere

Este archivo contiene la configuración WSGI necesaria para que tu aplicación
funcione correctamente en PythonAnywhere.
"""

import sys
import os

# Agrega el directorio de tu aplicación al path
path = '/home/tuusuario/mysite'  # Cambia 'tuusuario' por tu nombre de usuario en PythonAnywhere
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
