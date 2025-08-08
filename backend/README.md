# Backend Molpi - Guía de Despliegue en PythonAnywhere

## 📋 Requisitos Previos

1. Cuenta en [PythonAnywhere](https://www.pythonanywhere.com/)
2. Plan que soporte Flask (Beginner o superior)

## 🚀 Pasos de Instalación

### 1. Subir archivos a PythonAnywhere

1. **Comprimir la carpeta backend:**
   - Comprimir toda la carpeta `backend/` en un archivo ZIP
   - Subir el ZIP a tu cuenta de PythonAnywhere

2. **Extraer archivos en PythonAnywhere:**
   ```bash
   cd ~
   unzip backend.zip
   mv backend/* .
   ```

### 2. Instalar dependencias

En la consola Bash de PythonAnywhere:

```bash
pip3.10 install --user flask flask-cors
```

### 3. Configurar aplicación web

1. Ve a la pestaña **"Web"** en tu dashboard de PythonAnywhere
2. Crea una nueva aplicación web
3. Selecciona **"Manual configuration"**
4. Selecciona **Python 3.10**

### 4. Configurar WSGI

1. Edita el archivo WSGI (en `/var/www/tuusuario_pythonanywhere_com_wsgi.py`)
2. Reemplaza el contenido con:

```python
import sys
import os

# Agrega el directorio de tu aplicación al path
path = '/home/tuusuario'  # Cambia 'tuusuario' por tu nombre de usuario
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
```

### 5. Actualizar CORS en app.py

En el archivo `app.py`, actualiza la configuración CORS con tu dominio de Netlify:

```python
CORS(app, origins=[
    "https://tu-sitio.netlify.app",     # Tu dominio de Netlify
    "https://www.molpi.com.ar",         # Dominio personalizado
    "http://localhost:3000",            # Para desarrollo
])
```

### 6. Verificar base de datos

Asegúrate de que el archivo `molpi.db` esté en el directorio raíz de tu cuenta PythonAnywhere.

### 7. Recargar aplicación

En la pestaña "Web", haz clic en **"Reload tu-app"**

## 🔗 URLs de API

Una vez desplegado, tu API estará disponible en:
- `https://tuusuario.pythonanywhere.com/api/productos`
- `https://tuusuario.pythonanywhere.com/api/testimonios`
- `https://tuusuario.pythonanywhere.com/api/promociones`

## 🔧 Endpoints Disponibles

### Productos
- `GET /api/productos` - Obtener todos los productos
- `GET /api/productos/linea/20x20` - Productos línea 20x20
- `GET /api/productos/linea/40x40` - Productos línea 40x40
- `GET /api/productos/linea/50x50` - Productos línea 50x50
- `GET /api/productos/piscinas` - Productos piscinas
- `GET /api/productos/revestimientos` - Productos revestimientos
- `GET /api/productos/placas-antihumedad` - Productos placas antihumedad
- `GET /api/productos/insumos` - Productos insumos
- `POST /api/productos` - Crear producto
- `PUT /api/productos/:id` - Actualizar producto
- `DELETE /api/productos/:id` - Eliminar producto

### Testimonios
- `GET /api/testimonios` - Obtener testimonios activos
- `GET /api/testimonios/admin` - Obtener todos (admin)
- `POST /api/testimonios` - Crear testimonio
- `PUT /api/testimonios/:id` - Actualizar testimonio
- `DELETE /api/testimonios/:id` - Eliminar testimonio

### Promociones
- `GET /api/promociones` - Obtener promociones activas
- `GET /api/promociones/admin` - Obtener todas (admin)
- `POST /api/promociones` - Crear promoción
- `PUT /api/promociones/:id` - Actualizar promoción
- `DELETE /api/promociones/:id` - Eliminar promoción

### Otros
- `GET /api/health` - Verificar estado de la API
- `POST /api/login` - Autenticación
- `GET /api/categorias` - Obtener categorías
- `GET /api/subcategorias` - Obtener subcategorías

## 🐛 Debugging

Para ver logs de errores:
1. Ve a la pestaña "Tasks" en PythonAnywhere
2. O revisa los logs de error en la pestaña "Web"

## 🔐 Seguridad

- Cambia el `SECRET_KEY` en `app.py`
- Considera agregar autenticación más robusta para endpoints de admin
- Configura HTTPS en PythonAnywhere (incluido en planes pagados)
