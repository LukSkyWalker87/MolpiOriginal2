#!/bin/bash

# Script de Deployment para Molpi - Actualización de Promociones
# Ejecutar en el servidor: bash deploy-promociones.sh

set -e  # Detener si hay errores

echo "🚀 Iniciando deployment de promociones..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Verificar directorio
echo -e "${BLUE}📁 Verificando directorio...${NC}"
if [ ! -d "/opt/molpi/MolpiOriginal2" ]; then
    echo -e "${RED}❌ Error: Directorio /opt/molpi/MolpiOriginal2 no encontrado${NC}"
    exit 1
fi
cd /opt/molpi/MolpiOriginal2
echo -e "${GREEN}✅ En directorio correcto${NC}"

# 2. Git pull
echo -e "${BLUE}📥 Obteniendo últimos cambios desde GitHub...${NC}"
git pull origin main
echo -e "${GREEN}✅ Cambios obtenidos${NC}"

# 3. Detener contenedores
echo -e "${BLUE}🛑 Deteniendo contenedores...${NC}"
docker compose down
echo -e "${GREEN}✅ Contenedores detenidos${NC}"

# 4. Eliminar imagen vieja
echo -e "${BLUE}🗑️  Eliminando imagen vieja...${NC}"
docker rmi molpioriginal2-molpi-app 2>/dev/null || echo "Imagen no encontrada, continuando..."
echo -e "${GREEN}✅ Imagen eliminada${NC}"

# 5. Limpiar sistema Docker
echo -e "${BLUE}🧹 Limpiando sistema Docker...${NC}"
docker system prune -f
echo -e "${GREEN}✅ Sistema limpiado${NC}"

# 6. Reconstruir sin caché
echo -e "${BLUE}🔨 Reconstruyendo contenedores SIN caché...${NC}"
docker compose build --no-cache
echo -e "${GREEN}✅ Contenedores reconstruidos${NC}"

# 7. Levantar contenedores
echo -e "${BLUE}▶️  Levantando contenedores...${NC}"
docker compose up -d
echo -e "${GREEN}✅ Contenedores en ejecución${NC}"

# 8. Esperar a que la app esté lista
echo -e "${BLUE}⏳ Esperando a que la app esté lista...${NC}"
sleep 10

# 9. Verificar archivo actualizado
echo -e "${BLUE}🔍 Verificando archivo promociones.html dentro del contenedor...${NC}"
if docker exec -it molpioriginal2-molpi-app-1 cat /app/www.molpi.com.ar/components/promociones.html | grep -q "🟢🟢🟢 SCRIPT DE PROMOCIONES CARGADO"; then
    echo -e "${GREEN}✅ Archivo actualizado correctamente - logs de debugging encontrados${NC}"
else
    echo -e "${RED}⚠️  Advertencia: No se encontraron los logs de debugging en el archivo${NC}"
    echo -e "${RED}   Puede que el archivo no se haya actualizado correctamente${NC}"
fi

# 10. Reiniciar nginx
echo -e "${BLUE}🔄 Reiniciando nginx del host...${NC}"
sudo systemctl restart nginx
echo -e "${GREEN}✅ Nginx reiniciado${NC}"

# 11. Verificar estado de nginx
echo -e "${BLUE}🔍 Verificando estado de nginx...${NC}"
if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx está corriendo correctamente${NC}"
else
    echo -e "${RED}❌ Error: Nginx no está corriendo${NC}"
    sudo systemctl status nginx
    exit 1
fi

# 12. Mostrar logs recientes
echo -e "${BLUE}📋 Mostrando logs recientes del contenedor...${NC}"
docker compose logs --tail=50 molpi-app

echo ""
echo -e "${GREEN}✅✅✅ DEPLOYMENT COMPLETADO ✅✅✅${NC}"
echo ""
echo "📝 Pasos siguientes:"
echo "   1. Abrir navegador en modo incógnito"
echo "   2. Ir a https://www.molpi.com.ar/admin"
echo "   3. Iniciar sesión"
echo "   4. Ir a la sección Promociones"
echo "   5. Abrir consola del navegador (F12)"
echo "   6. Verificar que aparezcan logs de debugging con emojis 🔵 🟢"
echo "   7. Verificar que se muestren las 2 promociones en la tabla"
echo ""
echo "🐛 Si hay problemas, revisar logs con:"
echo "   docker compose logs -f molpi-app"
