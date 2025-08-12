# 🚀 MIGRACIÓN A DOCKER + GOOGLE CLOUD

## 📦 ARQUITECTURA NUEVA
```
Docker Container:
├── Python Flask App (Puerto 8080)
├── Frontend (admin.html + assets)
├── Base de datos SQLite incluida
└── Nginx (opcional, proxy reverso)
```

## 🛠️ PASOS PARA DEPLOYMENT

### PASO 1: Preparar Frontend para Docker
Modificar `frontend/env.js`:
```javascript
window.env = {
    API_URL: ''  // URL vacía = misma URL que el frontend
};
```

### PASO 2: Construir Docker Local
```bash
# En el directorio raíz del proyecto
docker build -t molpi-app .
docker run -p 8080:8080 molpi-app
```

### PASO 3: Probar Local
- Frontend: http://localhost:8080
- API: http://localhost:8080/api/health
- Admin: http://localhost:8080/admin.html

### PASO 4: Deploy a Google Cloud Run
```bash
# Instalar Google Cloud CLI
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Construir y subir imagen
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/molpi-app

# Deploy a Cloud Run
gcloud run deploy molpi-app \
  --image gcr.io/YOUR_PROJECT_ID/molpi-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
```

## ✅ VENTAJAS DE ESTA SOLUCIÓN

1. **Todo en un solo lugar**: Frontend + Backend + DB
2. **Sin problemas de CORS**: Mismo dominio
3. **Escalable**: Google Cloud Run escala automáticamente  
4. **Confiable**: Docker garantiza el entorno
5. **Económico**: Solo pagas por uso
6. **Fácil deploy**: Un solo comando

## 🎯 ARCHIVOS CREADOS

- `Dockerfile` - Configuración del contenedor
- `requirements.txt` - Dependencias Python  
- `docker-compose.yml` - Para testing local
- `Python/app_docker.py` - App Flask optimizada para Docker

## 📋 PRÓXIMOS PASOS

1. **Modificar env.js** del frontend
2. **Probar Docker local** 
3. **Setup Google Cloud project**
4. **Deploy a Cloud Run**

¿Quieres que empecemos con el paso 1 (modificar frontend) o prefieres probar Docker local primero?
