#!/bin/bash
# Script para actualizar UAT con código nuevo

set -e

echo "======================================================================"
echo "🧪 ACTUALIZAR UAT"
echo "======================================================================"
echo ""

cd /opt/molpi/MolpiOriginal2

# 1. Actualizar código (editar manualmente ya que no hay git pull)
echo "📝 Asegúrate de haber actualizado el código en /opt/molpi/MolpiOriginal2"
echo ""
read -p "¿Código actualizado? (s/n): " respuesta

if [ "$respuesta" != "s" ]; then
    echo "❌ Actualización cancelada"
    exit 0
fi

# 2. Build nueva imagen
echo ""
echo "🏗️  Construyendo nueva imagen..."
docker build -t molpi-app:uat .
echo "✅ Imagen construida"
echo ""

# 3. Reiniciar UAT
echo "🔄 Reiniciando UAT..."
docker stop molpi-uat
docker rm molpi-uat

docker run -d \
  --name molpi-uat \
  --restart unless-stopped \
  -p 127.0.0.1:8081:8080 \
  -v /opt/molpi/uat/data:/app/backend/data \
  -v /opt/molpi/uat/logs:/app/logs \
  -e FLASK_ENV=development \
  -e ENVIRONMENT=uat \
  molpi-app:uat

echo "✅ UAT actualizado"
echo ""

# 4. Verificar
echo "🔍 Verificando estado..."
sleep 3
docker ps | grep molpi-uat
echo ""

echo "======================================================================"
echo "✅ ¡UAT ACTUALIZADO!"
echo "======================================================================"
echo ""
echo "🧪 Prueba en: https://uat.molpi.com.ar"
echo "📊 Ver logs: docker logs -f molpi-uat"
echo ""
echo "✅ Si todo funciona bien en UAT, puedes promover a producción con:"
echo "   /opt/molpi/MolpiOriginal2/promover-a-prod.sh"
echo ""
