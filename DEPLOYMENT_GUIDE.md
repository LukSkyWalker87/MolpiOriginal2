# 🏗️ Molpi - Separación Frontend/Backend para Netlify + PythonAnywhere

## 📁 Estructura del Proyecto

Tu proyecto ha sido reorganizado para separar completamente el frontend del backend:

```
MolpiOriginal2/
├── 📂 backend/           # API REST para PythonAnywhere
│   ├── app.py           # Aplicación Flask optimizada
│   ├── wsgi.py          # Configuración WSGI
│   ├── requirements.txt # Dependencias Python
│   ├── molpi.db        # Base de datos SQLite
│   └── README.md       # Guía de despliegue
│
├── 📂 frontend/          # Sitio web estático para Netlify
│   ├── index.html      # Página principal
│   ├── admin.html      # Panel de administración
│   ├── env.js          # Configuración API (PRODUCCIÓN)
│   ├── _redirects      # Configuración Netlify
│   ├── css/            # Estilos
│   ├── js/             # Scripts
│   ├── img/            # Imágenes
│   └── README.md       # Guía de despliegue
│
└── 📂 Python/            # Código original (mantener como backup)
```

## 🚀 Plan de Despliegue

### 1️⃣ Backend en PythonAnywhere

1. **Subir archivos:**
   - Comprimir carpeta `backend/`
   - Subir a PythonAnywhere
   - Extraer en directorio home

2. **Instalar dependencias:**
   ```bash
   pip3.10 install --user flask flask-cors
   ```

3. **Configurar aplicación web:**
   - Crear nueva web app (Manual configuration)
   - Python 3.10
   - Configurar archivo WSGI

4. **Actualizar CORS:**
   ```python
   CORS(app, origins=[
       "https://tu-sitio.netlify.app",  # Tu dominio Netlify
       "https://www.molpi.com.ar"       # Dominio personalizado
   ])
   ```

### 2️⃣ Frontend en Netlify

1. **Crear repositorio:**
   ```bash
   cd frontend/
   git init
   git add .
   git commit -m "Frontend para Netlify"
   git remote add origin https://github.com/usuario/molpi-frontend.git
   git push -u origin main
   ```

2. **Configurar Netlify:**
   - Conectar repositorio GitHub
   - Build command: (vacío)
   - Publish directory: `.`

3. **Actualizar API URL:**
   ```javascript
   // En env.js
   window.env = {
       API_URL: 'https://tuusuario.pythonanywhere.com/api'
   };
   ```

## 🔗 URLs Finales

- **Frontend:** `https://tu-sitio.netlify.app`
- **Backend API:** `https://tuusuario.pythonanywhere.com/api`
- **Admin:** `https://tu-sitio.netlify.app/admin`

## ✅ Lo que se ha optimizado

### Backend (`/backend/`)
- ✅ API REST completa con prefijo `/api`
- ✅ CORS configurado para Netlify
- ✅ Eliminadas rutas de archivos estáticos
- ✅ Optimizado para PythonAnywhere
- ✅ SQLite incluida
- ✅ Error handlers

### Frontend (`/frontend/`)
- ✅ Todos los archivos estáticos (HTML, CSS, JS, imágenes)
- ✅ URLs de API actualizadas para usar `window.env.API_URL`
- ✅ Configuración Netlify (`_redirects`)
- ✅ Optimizado para deployment estático
- ✅ Headers de seguridad configurados

## 🔧 Desarrollo Local

### Backend
```bash
cd backend/
python app.py
# API disponible en http://127.0.0.1:5000/api
```

### Frontend
```bash
cd frontend/
# Cambiar env.js a: API_URL: 'http://127.0.0.1:5000/api'
python -m http.server 8000
# Frontend disponible en http://127.0.0.1:8000
```

## 🛡️ Características de Seguridad

- CORS configurado adecuadamente
- Headers de seguridad en Netlify
- Autenticación para endpoints de administración
- Validación de datos en backend

## 📋 Endpoints de API

### Públicos
- `GET /api/productos` - Productos activos
- `GET /api/productos/linea/{tamaño}` - Por línea específica
- `GET /api/productos/{categoria}` - Por categoría
- `GET /api/testimonios` - Testimonios activos
- `GET /api/promociones` - Promociones activas
- `GET /api/health` - Estado de la API

### Administración (requieren autenticación)
- `POST /api/login` - Autenticación
- `POST /api/productos` - Crear producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto
- `GET /api/testimonios/admin` - Todos los testimonios
- `POST /api/testimonios` - Crear testimonio
- `PUT /api/testimonios/{id}` - Actualizar testimonio
- `DELETE /api/testimonios/{id}` - Eliminar testimonio

## 🐛 Troubleshooting

### Error CORS
- Verificar que el dominio de Netlify esté en la configuración CORS del backend
- Asegurar que las URLs en `env.js` sean correctas

### API no responde
- Verificar estado: `https://tuusuario.pythonanywhere.com/api/health`
- Revisar logs en PythonAnywhere
- Verificar que la base de datos esté accesible

### Build falla en Netlify
- Verificar que no haya errores en JavaScript
- Asegurar que todas las rutas de archivos sean correctas
- Revisar el archivo `_redirects`

## 🎯 Próximos Pasos

1. **Desplegar Backend:**
   - Subir carpeta `backend/` a PythonAnywhere
   - Configurar aplicación web
   - Probar endpoints

2. **Desplegar Frontend:**
   - Crear repositorio para `frontend/`
   - Conectar a Netlify
   - Actualizar URL de API

3. **Configurar Dominio (Opcional):**
   - Configurar dominio personalizado en Netlify
   - Actualizar CORS en backend
   - Configurar SSL

4. **Optimizaciones Futuras:**
   - CDN para imágenes
   - Cache de API responses
   - Mejores métricas y analytics
   - Autenticación más robusta

## 📞 Soporte

Si necesitas ayuda:
1. Revisar los README.md de cada carpeta
2. Verificar logs de error
3. Probar endpoints individualmente
4. Contactar soporte de PythonAnywhere/Netlify

---

**¡Tu proyecto está listo para el despliegue!** 🚀
