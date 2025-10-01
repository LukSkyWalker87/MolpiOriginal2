# Script PowerShell para deployment en VPS
# Ejecutar desde Windows

param(
    [string]$Action = "deploy"
)

$VPS_HOST = "179.43.112.121"
$VPS_USER = "root"
$VPS_PORT = "5690"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Green "🚀 Molpi VPS Deployment Script"
Write-ColorOutput Yellow "================================"

switch ($Action) {
    "deploy" {
        Write-ColorOutput Cyan "`n📤 Subiendo script de deployment..."
        scp -P $VPS_PORT deploy-vps.sh ${VPS_USER}@${VPS_HOST}:/tmp/
        
        Write-ColorOutput Cyan "`n🔌 Conectando al servidor y ejecutando deployment..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "chmod +x /tmp/deploy-vps.sh && /tmp/deploy-vps.sh"
        
        Write-ColorOutput Green "`n✅ Deployment completado!"
        Write-ColorOutput Yellow "`n🌐 Tu aplicación está disponible en:"
        Write-ColorOutput White "   http://$VPS_HOST"
        Write-ColorOutput White "   http://vps-5346672-x.dattaweb.com"
    }
    
    "update" {
        Write-ColorOutput Cyan "`n🔄 Actualizando aplicación..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} @"
cd /opt/molpi/MolpiOriginal2
git pull
docker build -t molpi-app:latest .
docker stop molpi-prod
docker rm molpi-prod
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v /opt/molpi/data:/app/backend/data \
  molpi-app:latest
"@
        Write-ColorOutput Green "`n✅ Aplicación actualizada!"
    }
    
    "logs" {
        Write-ColorOutput Cyan "`n📊 Mostrando logs (Ctrl+C para salir)..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "docker logs -f molpi-prod"
    }
    
    "status" {
        Write-ColorOutput Cyan "`n📊 Estado del servidor..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} @"
echo "=== Docker Containers ==="
docker ps
echo ""
echo "=== Disk Usage ==="
df -h | grep -E '^Filesystem|/dev/vda'
echo ""
echo "=== Memory Usage ==="
free -h
echo ""
echo "=== Application Status ==="
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:5000
"@
    }
    
    "restart" {
        Write-ColorOutput Cyan "`n🔄 Reiniciando aplicación..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "docker restart molpi-prod"
        Write-ColorOutput Green "`n✅ Aplicación reiniciada!"
    }
    
    "stop" {
        Write-ColorOutput Cyan "`n🛑 Deteniendo aplicación..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "docker stop molpi-prod"
        Write-ColorOutput Yellow "`n⚠️ Aplicación detenida!"
    }
    
    "start" {
        Write-ColorOutput Cyan "`n▶️ Iniciando aplicación..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "docker start molpi-prod"
        Write-ColorOutput Green "`n✅ Aplicación iniciada!"
    }
    
    "backup" {
        Write-ColorOutput Cyan "`n💾 Creando backup de la base de datos..."
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST} "docker cp molpi-prod:/app/backend/molpi.db /opt/molpi/backups/molpi_$timestamp.db"
        
        Write-ColorOutput Cyan "`n📥 Descargando backup..."
        scp -P $VPS_PORT ${VPS_USER}@${VPS_HOST}:/opt/molpi/backups/molpi_$timestamp.db ./backups/
        
        Write-ColorOutput Green "`n✅ Backup completado: ./backups/molpi_$timestamp.db"
    }
    
    "ssh" {
        Write-ColorOutput Cyan "`n🔌 Conectando al servidor..."
        ssh -p $VPS_PORT ${VPS_USER}@${VPS_HOST}
    }
    
    default {
        Write-ColorOutput Yellow @"

📖 Uso: .\deploy-vps.ps1 -Action <comando>

Comandos disponibles:

  deploy    - Deployment inicial de la aplicación
  update    - Actualizar aplicación (git pull + rebuild)
  logs      - Ver logs en tiempo real
  status    - Ver estado del servidor y aplicación
  restart   - Reiniciar aplicación
  stop      - Detener aplicación
  start     - Iniciar aplicación
  backup    - Crear y descargar backup de la BD
  ssh       - Conectar al servidor por SSH

Ejemplos:
  .\deploy-vps.ps1 -Action deploy
  .\deploy-vps.ps1 -Action logs
  .\deploy-vps.ps1 -Action status

"@
    }
}
