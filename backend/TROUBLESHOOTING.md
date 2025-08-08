# 🚨 Solución de Error Backend PythonAnywhere

## Problema Detectado
Error "Unhandled Exception" en PythonAnywhere al intentar acceder a la API.

## ✅ Pasos para Solucionarlo

### 1. Actualizar archivo WSGI en PythonAnywhere

En tu panel de PythonAnywhere, ve a la pestaña **"Web"** y edita el archivo WSGI. Reemplaza todo el contenido con:

```python
# -*- coding: utf-8 -*-
import sys
import os

# Agrega el directorio de tu aplicación al path
path = '/home/sgit'  # Tu nombre de usuario
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
```

### 2. Verificar archivos en PythonAnywhere

Asegúrate de que tienes estos archivos en `/home/sgit/`:
- ✅ `app.py`
- ✅ `molpi.db`
- ✅ (Opcional) `requirements.txt`

### 3. Instalar dependencias (si no lo has hecho)

En la consola Bash de PythonAnywhere:

```bash
pip3.10 install --user flask flask-cors
```

### 4. Verificar permisos de la base de datos

```bash
ls -la /home/sgit/molpi.db
chmod 664 /home/sgit/molpi.db
```

### 5. Recargar la aplicación

En la pestaña "Web" de PythonAnywhere, hacer clic en el botón **"Reload"**.

### 6. Verificar logs

En PythonAnywhere, ve a:
- Pestaña "Web" → "Log files"
- Revisa `error.log` y `server.log`

### 7. Test de verificación

Abre en el navegador:
```
https://sgit.pythonanywhere.com/api/health
```

Deberías ver una respuesta JSON como:
```json
{
  "status": "OK",
  "message": "Molpi API is running",
  "timestamp": "2025-08-08T...",
  "database": "Connected"
}
```

## 🔧 Debugging

Si sigue sin funcionar:

1. **Revisar logs:**
   - Ve a la pestaña "Tasks" en PythonAnywhere
   - Revisa los mensajes de error

2. **Test manual:**
   - Abre una consola Bash en PythonAnywhere
   - Ejecuta: `cd /home/sgit && python3.10 app.py`
   - Ve si hay errores en la consola

3. **Verificar base de datos:**
   ```bash
   python3.10 -c "import sqlite3; conn = sqlite3.connect('molpi.db'); print('DB OK')"
   ```

## 📞 Contacto

Si el problema persiste, envía:
- Screenshot de los logs de error
- Contenido del archivo WSGI actual
- Resultado del comando de verificación de DB

---

**¡Una vez solucionado, tu API estará disponible en:**
`https://sgit.pythonanywhere.com/api`
