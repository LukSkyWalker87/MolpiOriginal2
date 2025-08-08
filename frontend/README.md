# Frontend Molpi - Guía de Despliegue en Netlify

## 📋 Descripción

Este es el frontend de la aplicación Molpi, optimizado para ser desplegado en Netlify y conectarse con el backend en PythonAnywhere.

## 🚀 Pasos de Despliegue en Netlify

### 1. Preparar el repositorio

1. **Crear un nuevo repositorio en GitHub solo para el frontend:**
   ```bash
   git init
   git add .
   git commit -m "Initial frontend commit"
   git remote add origin https://github.com/tuusuario/molpi-frontend.git
   git push -u origin main
   ```

### 2. Configurar Netlify

1. Ve a [Netlify](https://www.netlify.com/)
2. Conecta tu cuenta de GitHub
3. Selecciona "New site from Git"
4. Elige tu repositorio del frontend
5. Configuración de build:
   - **Build command:** (dejar vacío)
   - **Publish directory:** `.` (punto, directorio raíz)
   - **Branch to deploy:** `main`

### 3. Configurar variables de entorno

Antes del despliegue, **IMPORTANTE:** actualizar `env.js`:

```javascript
// En env.js, cambiar:
window.env = {
    API_URL: 'https://tuusuario.pythonanywhere.com/api'  // Tu backend de PythonAnywhere
};
```

### 4. Configurar dominio personalizado (Opcional)

Si tienes un dominio personalizado:
1. Ve a "Domain management" en Netlify
2. Agrega tu dominio personalizado
3. Configura los DNS según las instrucciones de Netlify

## 🔧 Estructura del Proyecto

```
frontend/
├── index.html                 # Página principal
├── admin.html                 # Panel de administración
├── env.js                     # Configuración API (PRODUCCIÓN)
├── env.local.js              # Configuración API (DESARROLLO)
├── _redirects                # Configuración de rutas Netlify
├── css/                      # Estilos
├── js/                       # Scripts JavaScript
├── img/                      # Imágenes
├── components/               # Componentes reutilizables
├── vendor/                   # Librerías externas
└── pdf/                      # Archivos PDF
```

## 🌍 URLs de Producción

Una vez desplegado en Netlify, tendrás:
- **Frontend:** `https://tu-sitio.netlify.app`
- **Backend API:** `https://tuusuario.pythonanywhere.com/api`

## 🔄 Desarrollo Local

Para desarrollo local:

1. **Usar servidor local:**
   ```bash
   # Opción 1: Python
   python -m http.server 8000
   
   # Opción 2: Node.js (si tienes instalado)
   npx serve .
   
   # Opción 3: PHP
   php -S localhost:8000
   ```

2. **Cambiar configuración API:**
   - Renombrar `env.js` a `env.prod.js`
   - Renombrar `env.local.js` a `env.js`
   - O editar directamente `env.js` para apuntar a `http://127.0.0.1:5000`

## 🎯 Endpoints de API

El frontend consume estos endpoints del backend:

### Productos
- `GET /api/productos` - Todos los productos
- `GET /api/productos/linea/20x20` - Productos 20x20
- `GET /api/productos/linea/40x40` - Productos 40x40
- `GET /api/productos/linea/50x50` - Productos 50x50
- `GET /api/productos/piscinas` - Productos piscinas
- `GET /api/productos/revestimientos` - Productos revestimientos
- `GET /api/productos/placas-antihumedad` - Placas antihumedad
- `GET /api/productos/insumos` - Insumos

### Testimonios
- `GET /api/testimonios` - Testimonios activos
- `GET /api/testimonios/admin` - Todos los testimonios (admin)

### Promociones
- `GET /api/promociones` - Promociones activas
- `GET /api/promociones/admin` - Todas las promociones (admin)

### Administración
- `POST /api/login` - Autenticación
- `POST /api/productos` - Crear producto
- `PUT /api/productos/:id` - Actualizar producto
- `DELETE /api/productos/:id` - Eliminar producto

## 🛠️ Configuración de CORS

El backend está configurado para aceptar requests desde:
- Tu dominio de Netlify
- `localhost` para desarrollo
- Dominios personalizados

## 🐛 Troubleshooting

### Error de CORS
Si tienes errores de CORS, asegúrate de que:
1. El backend tenga configurado tu dominio de Netlify en `CORS(app, origins=[...])`
2. Las URLs en `env.js` sean correctas

### API no responde
1. Verifica que el backend esté funcionando: `https://tuusuario.pythonanywhere.com/api/health`
2. Revisa los logs en PythonAnywhere
3. Verifica que la base de datos esté accesible

### Imágenes no cargan
1. Asegúrate de que todas las imágenes estén en la carpeta `img/`
2. Verifica las rutas relativas en el HTML
3. Considera usar un CDN para imágenes pesadas

## 📱 Responsive Design

El sitio está optimizado para:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px - 1024px)
- ✅ Mobile (320px - 767px)

## 🔐 Seguridad

### Headers configurados:
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

### Consideraciones:
- Autenticación básica para admin (considera mejorar en producción)
- Validación de datos en frontend y backend
- HTTPS forzado en Netlify

## 🚀 Deploy Automático

Para configurar deploy automático:
1. Conecta el repositorio a Netlify
2. Cada push a `main` desplegará automáticamente
3. Netlify mostrará previews de pull requests

## 📊 Analytics

Para agregar analytics:
1. Agrega Google Analytics en `index.html`
2. O usa Netlify Analytics (plan pagado)

## 🔧 Optimizaciones

### Performance:
- Imágenes optimizadas (WebP cuando sea posible)
- CSS y JS minificados en vendor/
- Lazy loading para imágenes de productos

### SEO:
- Meta tags configurados
- URLs amigables
- Sitemap.xml (agregar si es necesario)
