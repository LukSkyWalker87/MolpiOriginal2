#!/bin/bash
# Script para deploy en UAT

set -e

AMBIENTE="UAT"
CONTENEDOR="molpi-uat"
PUERTO="8081"
DATA_DIR="/opt/molpi/uat/data"
LOGS_DIR="/opt/molpi/uat/logs"

echo "======================================================================"
echo "🧪 DEPLOYMENT A UAT"
echo "======================================================================"
echo ""

# Ir al directorio del proyecto
cd /opt/molpi/MolpiOriginal2

# Actualizar código
echo "📥 Actualizando código desde GitHub..."
git pull origin main
echo "✅ Código actualizado"
echo ""

# Build nueva imagen
echo "🏗️  Construyendo nueva imagen..."
docker build -t molpi-app:uat .
echo "✅ Imagen construida"
echo ""

# Detener contenedor anterior
echo "🛑 Deteniendo contenedor de UAT..."
docker stop $CONTENEDOR 2>/dev/null || true
docker rm $CONTENEDOR 2>/dev/null || true
echo "✅ Contenedor detenido"
echo ""

# Iniciar nuevo contenedor
echo "▶️  Iniciando nuevo contenedor de UAT..."
docker run -d \
  --name $CONTENEDOR \
  --restart unless-stopped \
  -p 127.0.0.1:$PUERTO:8080 \
  -v $DATA_DIR:/app/backend/data \
  -v $LOGS_DIR:/app/logs \
  -e FLASK_ENV=development \
  -e ENVIRONMENT=uat \
  molpi-app:uat

echo "✅ Contenedor iniciado"
echo ""

# Verificar
echo "🔍 Verificando estado..."
sleep 3
docker ps | grep $CONTENEDOR
echo ""

echo "📝 Primeras líneas de logs:"
docker logs $CONTENEDOR | head -n 15
echo ""

echo "======================================================================"
echo "✅ ¡DEPLOYMENT A UAT COMPLETADO!"
echo "======================================================================"
echo ""
echo "🌐 URL: https://uat.molpi.com.ar"
echo "📊 Ver logs: docker logs -f $CONTENEDOR"
echo "🔄 Reiniciar: docker restart $CONTENEDOR"
echo ""
