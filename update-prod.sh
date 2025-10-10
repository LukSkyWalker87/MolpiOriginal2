#!/bin/bash
# Script rápido para actualizar producción

set -e

echo "======================================================================"
echo "🚀 ACTUALIZANDO PRODUCCIÓN"
echo "======================================================================"
echo ""

cd /opt/molpi/MolpiOriginal2

# 1. Actualizar código
echo "📥 Actualizando código desde GitHub..."
git pull origin main
echo "✅ Código actualizado"
echo ""

# 2. Rebuild imagen
echo "🏗️  Reconstruyendo imagen Docker..."
docker build -t molpi-app:latest .
echo "✅ Imagen reconstruida"
echo ""

# 3. Reiniciar contenedor
echo "🔄 Reiniciando aplicación..."
docker stop molpi-prod
docker rm molpi-prod

docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v /opt/molpi/data:/app/backend/data \
  -v /opt/molpi/logs:/app/logs \
  -e FLASK_ENV=production \
  molpi-app:latest

echo "✅ Aplicación reiniciada"
echo ""

# 4. Verificar
echo "🔍 Verificando estado..."
sleep 3
docker ps | grep molpi-prod
echo ""

echo "======================================================================"
echo "✅ ¡ACTUALIZACIÓN COMPLETADA!"
echo "======================================================================"
echo ""
echo "🌐 https://molpi.com.ar"
echo "📊 Ver logs: docker logs -f molpi-prod"
echo ""
echo "🔐 Nuevas credenciales:"
echo "   Usuario: admin"
echo "   Contraseña: dumba3110"
echo ""
