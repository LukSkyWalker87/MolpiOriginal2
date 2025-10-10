#!/bin/bash
# Script de deployment automático para Molpi
# Ejecutar en el servidor VPS

set -e  # Detener si hay error

echo "======================================================================"
echo "🚀 DEPLOYMENT AUTOMÁTICO DE MOLPI"
echo "======================================================================"
echo ""

# Paso 1: Limpiar directorio anterior
echo "📁 Paso 1/9: Limpiando directorio anterior..."
cd /opt/molpi
rm -rf MolpiOriginal2
echo "✅ Directorio limpiado"
echo ""

# Paso 2: Clonar repositorio
echo "📥 Paso 2/9: Clonando repositorio desde GitHub..."
git clone https://github.com/LukSkyWalker87/MolpiOriginal2.git
echo "✅ Repositorio clonado"
echo ""

# Paso 3: Entrar al directorio
echo "📂 Paso 3/9: Entrando al directorio..."
cd MolpiOriginal2
echo "✅ Directorio actual: $(pwd)"
echo ""

# Paso 4: Verificar Dockerfile
echo "🔍 Paso 4/9: Verificando Dockerfile..."
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile encontrado"
    echo "Contenido de las primeras líneas:"
    head -n 5 Dockerfile
else
    echo "❌ ERROR: Dockerfile no encontrado"
    exit 1
fi
echo ""

# Paso 5: Build de imagen Docker
echo "🏗️  Paso 5/9: Construyendo imagen Docker..."
echo "⏳ Esto puede tomar varios minutos, por favor espera..."
docker build -t molpi-app:latest .
echo "✅ Imagen construida exitosamente"
echo ""

# Paso 6: Verificar imagen
echo "🔍 Paso 6/9: Verificando imagen creada..."
docker images | grep molpi
echo "✅ Imagen verificada"
echo ""

# Paso 7: Crear directorios
echo "📁 Paso 7/9: Creando directorios para datos..."
mkdir -p /opt/molpi/data
mkdir -p /opt/molpi/backups
mkdir -p /opt/molpi/logs
echo "✅ Directorios creados"
echo ""

# Paso 8: Detener contenedor anterior si existe
echo "🛑 Paso 8/9: Deteniendo contenedor anterior (si existe)..."
docker stop molpi-prod 2>/dev/null || echo "No hay contenedor anterior"
docker rm molpi-prod 2>/dev/null || echo "No hay contenedor para eliminar"
echo "✅ Contenedor anterior eliminado"
echo ""

# Paso 9: Ejecutar nuevo contenedor
echo "▶️  Paso 9/9: Iniciando aplicación..."
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v /opt/molpi/data:/app/backend/data \
  -v /opt/molpi/logs:/app/logs \
  -e FLASK_ENV=production \
  molpi-app:latest

echo "✅ Aplicación iniciada"
echo ""

# Verificación final
echo "======================================================================"
echo "🔍 VERIFICACIÓN FINAL"
echo "======================================================================"
echo ""

echo "📊 Estado del contenedor:"
docker ps | grep molpi-prod
echo ""

echo "📝 Primeras líneas de logs:"
sleep 3
docker logs molpi-prod | head -n 20
echo ""

echo "🌐 Probando conexión local..."
sleep 2
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200"; then
    echo "✅ Aplicación respondiendo correctamente"
else
    echo "⚠️  Aplicación puede estar iniciando, verifica los logs"
fi
echo ""

echo "======================================================================"
echo "✅ ¡DEPLOYMENT COMPLETADO!"
echo "======================================================================"
echo ""
echo "🌐 Tu aplicación está disponible en:"
echo "   - http://179.43.112.121"
echo "   - http://vps-5346672-x.dattaweb.com"
echo ""
echo "📊 Comandos útiles:"
echo "   Ver logs:      docker logs -f molpi-prod"
echo "   Reiniciar:     docker restart molpi-prod"
echo "   Estado:        docker ps"
echo "   Entrar:        docker exec -it molpi-prod bash"
echo ""
