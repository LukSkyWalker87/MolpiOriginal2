#!/bin/bash
# Script de deployment simplificado para VPS Dattaweb
# Molpi Application - Ubuntu 24.04 con Docker

set -e

echo "🚀 Iniciando deployment de Molpi..."
echo "===================================="

# 1. Verificar Docker
echo ""
echo "✓ Verificando Docker..."
docker --version || { echo "❌ Docker no encontrado"; exit 1; }

# 2. Crear directorios
echo "✓ Creando estructura de directorios..."
mkdir -p /opt/molpi/{data,backups,logs}

# 3. Clonar o actualizar repositorio
echo "✓ Obteniendo código fuente..."
if [ -d "/opt/molpi/MolpiOriginal2" ]; then
    echo "  → Actualizando repositorio existente..."
    cd /opt/molpi/MolpiOriginal2
    git pull origin main
else
    echo "  → Clonando repositorio..."
    cd /opt/molpi
    git clone https://github.com/LukSkyWalker87/MolpiOriginal2.git
    cd MolpiOriginal2
fi

# 4. Build de la imagen
echo "✓ Construyendo imagen Docker..."
docker build -t molpi-app:latest .

# 5. Detener contenedor anterior
echo "✓ Deteniendo contenedor anterior (si existe)..."
docker stop molpi-prod 2>/dev/null || true
docker rm molpi-prod 2>/dev/null || true

# 6. Ejecutar nuevo contenedor
echo "✓ Iniciando aplicación..."
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v /opt/molpi/data:/app/backend \
  -v /opt/molpi/logs:/app/logs \
  -e FLASK_ENV=production \
  molpi-app:latest

# 7. Esperar y verificar
echo "✓ Esperando inicio de la aplicación..."
sleep 5

echo ""
echo "✓ Verificando estado..."
docker ps | grep molpi-prod

echo ""
echo "✅ ¡DEPLOYMENT COMPLETADO!"
echo "===================================="
echo ""
echo "🌐 Accede a tu aplicación en:"
echo "   • http://179.43.112.121"
echo "   • http://vps-5346672-x.dattaweb.com"
echo ""
echo "📊 Comandos útiles:"
echo "   • Ver logs:      docker logs -f molpi-prod"
echo "   • Reiniciar:     docker restart molpi-prod"
echo "   • Estado:        docker ps"
echo "   • Detener:       docker stop molpi-prod"
echo ""
