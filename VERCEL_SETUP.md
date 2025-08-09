# Configuración de Vercel para Molpi

## Configuración del Proyecto

**Root Directory**: Déjalo vacío (usará la raíz del proyecto)
**Framework Preset**: Other
**Build Command**: Déjalo vacío (es HTML estático)
**Output Directory**: Déjalo vacío
**Install Command**: Déjalo vacío

## Estructura

- `/frontend/` - Archivos del frontend (HTML, CSS, JS)
- `/backend/` - Código del backend (para referencia, no se despliega en Vercel)
- `vercel.json` - Configuración de rutas y headers para Vercel

## Variables de Entorno en Vercel

No necesitas configurar variables de entorno específicas, ya que la configuración está en `frontend/env.js`.

## URLs después del deploy

- **Frontend principal**: `https://tu-proyecto.vercel.app`
- **Panel admin**: `https://tu-proyecto.vercel.app/admin.html`
- **API Backend**: `https://sgit.pythonanywhere.com/api` (ya configurado)

## Configuración CORS

El backend en PythonAnywhere ya está configurado para aceptar peticiones desde cualquier dominio de Vercel.
