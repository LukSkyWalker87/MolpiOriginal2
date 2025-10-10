#!/bin/bash
# Script para promover UAT a Producción

set -e

echo "======================================================================"
echo "🚀 PROMOCIÓN DE UAT A PRODUCCIÓN"
echo "======================================================================"
echo ""
echo "⚠️  ADVERTENCIA: Esto va a:"
echo "   1. Hacer backup de Producción actual"
echo "   2. Copiar la BD de UAT a Producción"
echo "   3. Reiniciar el contenedor de Producción"
echo ""
read -p "¿Deseas continuar? (escribe 'SI' para confirmar): " confirmacion

if [ "$confirmacion" != "SI" ]; then
    echo "❌ Promoción cancelada"
    exit 0
fi

echo ""
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Backup de producción
echo "💾 Creando backup de Producción..."
cp /opt/molpi/produccion/data/molpi.db /opt/molpi/produccion/backups/molpi_pre_promocion_${TIMESTAMP}.db
echo "✅ Backup creado: molpi_pre_promocion_${TIMESTAMP}.db"
echo ""

# 2. Copiar BD de UAT a Producción
echo "📋 Copiando BD de UAT a Producción..."
docker stop molpi-prod
cp /opt/molpi/uat/data/molpi.db /opt/molpi/produccion/data/molpi.db
echo "✅ BD copiada"
echo ""

# 3. Reiniciar producción
echo "🔄 Reiniciando Producción..."
docker start molpi-prod
sleep 3
echo "✅ Producción reiniciada"
echo ""

# 4. Verificar
echo "🔍 Verificando estado..."
docker ps | grep molpi
echo ""

echo "======================================================================"
echo "✅ ¡PROMOCIÓN COMPLETADA!"
echo "======================================================================"
echo ""
echo "🏭 Los cambios de UAT ahora están en Producción"
echo "🌐 Verifica en: https://molpi.com.ar"
echo ""
echo "💾 Backup disponible en:"
echo "   /opt/molpi/produccion/backups/molpi_pre_promocion_${TIMESTAMP}.db"
echo ""
echo "🔙 Para revertir si hay problemas:"
echo "   docker stop molpi-prod"
echo "   cp /opt/molpi/produccion/backups/molpi_pre_promocion_${TIMESTAMP}.db /opt/molpi/produccion/data/molpi.db"
echo "   docker start molpi-prod"
echo ""
