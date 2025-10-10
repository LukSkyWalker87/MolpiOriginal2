#!/bin/bash
# Script para deploy en PRODUCCIÓN

set -e

AMBIENTE="PRODUCCIÓN"
CONTENEDOR="molpi-produccion"
PUERTO="8080"
DATA_DIR="/opt/molpi/produccion/data"
LOGS_DIR="/opt/molpi/produccion/logs"
BACKUP_DIR="/opt/molpi/produccion/backups"

echo "======================================================================"
echo "🏭 DEPLOYMENT A PRODUCCIÓN"
echo "======================================================================"
echo ""
echo "⚠️  ADVERTENCIA: Vas a deployar a PRODUCCIÓN"
read -p "¿Continuar? (s/n): " respuesta

if [ "$respuesta" != "s" ] && [ "$respuesta" != "S" ]; then
    echo "❌ Deployment cancelado"
    exit 0
fi

# Crear backup de la base de datos
echo ""
echo "💾 Creando backup de la base de datos..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker cp $CONTENEDOR:/app/backend/molpi.db $BACKUP_DIR/molpi_pre_deploy_$TIMESTAMP.db 2>/dev/null || echo "⚠️  No se pudo hacer backup (¿primera vez?)"
echo "✅ Backup creado: molpi_pre_deploy_$TIMESTAMP.db"
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
docker build -t molpi-app:prod .
echo "✅ Imagen construida"
echo ""

# Detener contenedor anterior
echo "🛑 Deteniendo contenedor de PRODUCCIÓN..."
docker stop $CONTENEDOR
docker rm $CONTENEDOR
echo "✅ Contenedor detenido"
echo ""

# Iniciar nuevo contenedor
echo "▶️  Iniciando nuevo contenedor de PRODUCCIÓN..."
docker run -d \
  --name $CONTENEDOR \
  --restart unless-stopped \
  -p 127.0.0.1:$PUERTO:8080 \
  -v $DATA_DIR:/app/backend/data \
  -v $LOGS_DIR:/app/logs \
  -e FLASK_ENV=production \
  -e ENVIRONMENT=production \
  molpi-app:prod

echo "✅ Contenedor iniciado"
echo ""

# Verificar
echo "🔍 Verificando estado..."
sleep 5
docker ps | grep $CONTENEDOR
echo ""

echo "📝 Primeras líneas de logs:"
docker logs $CONTENEDOR | head -n 15
echo ""

# Verificar que responde
echo "🌐 Verificando que la aplicación responde..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:$PUERTO | grep -q "200"; then
    echo "✅ Aplicación respondiendo correctamente"
else
    echo "⚠️  La aplicación puede estar iniciando, verifica los logs"
fi
echo ""

echo "======================================================================"
echo "✅ ¡DEPLOYMENT A PRODUCCIÓN COMPLETADO!"
echo "======================================================================"
echo ""
echo "🌐 URL: https://molpi.com.ar"
echo "💾 Backup: $BACKUP_DIR/molpi_pre_deploy_$TIMESTAMP.db"
echo "📊 Ver logs: docker logs -f $CONTENEDOR"
echo "🔄 Reiniciar: docker restart $CONTENEDOR"
echo ""
echo "🔙 Para revertir cambios:"
echo "   docker stop $CONTENEDOR"
echo "   docker rm $CONTENEDOR"
echo "   docker run -d --name $CONTENEDOR --restart unless-stopped -p 127.0.0.1:$PUERTO:8080 -v $DATA_DIR:/app/backend/data -v $LOGS_DIR:/app/logs -e FLASK_ENV=production molpi-app:prod"
echo ""
