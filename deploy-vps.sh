#!/bin/bash
# Script de deployment para VPS con Docker
# Molpi Application - Ubuntu 24.04

set -e

echo "🚀 Iniciando deployment de Molpi en VPS..."

# 1. Actualizar sistema
echo "📦 Actualizando sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar dependencias básicas
echo "🔧 Instalando dependencias..."
sudo apt-get install -y git curl wget nano

# 3. Verificar Docker (ya debería estar instalado)
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
else
    echo "✅ Docker ya está instalado"
fi

# 4. Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📥 Instalando Docker Compose..."
    sudo apt-get install -y docker-compose-plugin
else
    echo "✅ Docker Compose ya está instalado"
fi

# 5. Crear directorios
echo "📁 Creando estructura de directorios..."
sudo mkdir -p /opt/molpi
sudo mkdir -p /opt/molpi/data
sudo mkdir -p /opt/molpi/backups
sudo mkdir -p /opt/molpi/logs

# 6. Clonar repositorio
echo "📥 Clonando repositorio..."
cd /opt/molpi
if [ -d "MolpiOriginal2" ]; then
    echo "📂 Repositorio existe, actualizando..."
    cd MolpiOriginal2
    git pull
else
    git clone https://github.com/LukSkyWalker87/MolpiOriginal2.git
    cd MolpiOriginal2
fi

# 7. Build de la imagen
echo "🏗️ Construyendo imagen Docker..."
sudo docker build -t molpi-app:latest .

# 8. Detener contenedor anterior si existe
echo "🛑 Deteniendo contenedor anterior..."
sudo docker stop molpi-prod 2>/dev/null || true
sudo docker rm molpi-prod 2>/dev/null || true

# 9. Ejecutar nuevo contenedor
echo "▶️ Iniciando aplicación..."
sudo docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -p 443:5000 \
  -v /opt/molpi/data:/app/backend/data \
  -v /opt/molpi/logs:/app/logs \
  -e FLASK_ENV=production \
  molpi-app:latest

# 10. Verificar estado
echo "🔍 Verificando estado del contenedor..."
sleep 5
sudo docker ps | grep molpi-prod

echo ""
echo "✅ ¡Deployment completado!"
echo "🌐 Tu aplicación está corriendo en:"
echo "   http://179.43.112.121"
echo "   http://vps-5346672-x.dattaweb.com"
echo ""
echo "📊 Ver logs: sudo docker logs -f molpi-prod"
echo "🔄 Reiniciar: sudo docker restart molpi-prod"
echo "🛑 Detener: sudo docker stop molpi-prod"
