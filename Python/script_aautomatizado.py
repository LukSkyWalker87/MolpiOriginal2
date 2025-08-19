# Script para copiar archivos de www.molpi.com.ar a backend para Flask
import os
import shutil


# Rutas origen y destino (robusto para cualquier ubicación de ejecución)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # MolpiOriginal2
ORIGEN = os.path.join(BASE_DIR, 'www.molpi.com.ar')
DEST_TEMPLATES = os.path.join(BASE_DIR, 'Python', 'backend', 'templates')
DEST_STATIC = os.path.join(BASE_DIR, 'Python', 'backend', 'static')


# 1. Limpiar y copiar solo los .html de www.molpi.com.ar a templates
for archivo in os.listdir(DEST_TEMPLATES):
	ruta = os.path.join(DEST_TEMPLATES, archivo)
	if os.path.isfile(ruta):
		os.unlink(ruta)
	elif os.path.isdir(ruta):
		shutil.rmtree(ruta)
for archivo in os.listdir(ORIGEN):
	if archivo.endswith('.html'):
		shutil.copy2(os.path.join(ORIGEN, archivo), os.path.join(DEST_TEMPLATES, archivo))

# 2. Copiar carpetas css, js, img a static

for carpeta in ['css', 'js', 'img']:
	origen_carpeta = os.path.join(ORIGEN, carpeta)
	destino_carpeta = os.path.join(DEST_STATIC, carpeta)
	if os.path.exists(origen_carpeta):
		if os.path.exists(destino_carpeta):
			# Borrar solo el contenido de la carpeta
			for nombre in os.listdir(destino_carpeta):
				ruta = os.path.join(destino_carpeta, nombre)
				try:
					if os.path.isfile(ruta) or os.path.islink(ruta):
						os.unlink(ruta)
					elif os.path.isdir(ruta):
						shutil.rmtree(ruta)
				except Exception as e:
					print(f'No se pudo borrar {ruta}: {e}')
		else:
			os.makedirs(destino_carpeta)
		# Copiar el contenido
		for nombre in os.listdir(origen_carpeta):
			src = os.path.join(origen_carpeta, nombre)
			dst = os.path.join(destino_carpeta, nombre)
			if os.path.isdir(src):
				shutil.copytree(src, dst, dirs_exist_ok=True)
			else:
				shutil.copy2(src, dst)

print('¡Copiado completo! Los templates y estáticos están listos para Flask.')