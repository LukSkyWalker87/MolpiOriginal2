#!/bin/bash
# Script para configurar ambientes UAT y Producción

set -e

echo "======================================================================"
echo "🔄 CONFIGURACIÓN DE AMBIENTES UAT Y PRODUCCIÓN"
echo "======================================================================"
echo ""

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p /opt/molpi/produccion/data
mkdir -p /opt/molpi/produccion/logs
mkdir -p /opt/molpi/produccion/backups
mkdir -p /opt/molpi/uat/data
mkdir -p /opt/molpi/uat/logs
mkdir -p /opt/molpi/uat/backups
echo "✅ Directorios creados"
echo ""

# Detener contenedor actual
echo "🛑 Deteniendo contenedor actual..."
docker stop molpi-prod 2>/dev/null || true
docker rm molpi-prod 2>/dev/null || true
echo "✅ Contenedor detenido"
echo ""

# Crear contenedor de PRODUCCIÓN
echo "🏭 Creando contenedor de PRODUCCIÓN..."
docker run -d \
  --name molpi-produccion \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v /opt/molpi/produccion/data:/app/backend/data \
  -v /opt/molpi/produccion/logs:/app/logs \
  -e FLASK_ENV=production \
  -e ENVIRONMENT=production \
  molpi-app:latest
echo "✅ Contenedor de producción creado en puerto 8080"
echo ""

# Crear contenedor de UAT
echo "🧪 Creando contenedor de UAT..."
docker run -d \
  --name molpi-uat \
  --restart unless-stopped \
  -p 127.0.0.1:8081:8080 \
  -v /opt/molpi/uat/data:/app/backend/data \
  -v /opt/molpi/uat/logs:/app/logs \
  -e FLASK_ENV=development \
  -e ENVIRONMENT=uat \
  molpi-app:latest
echo "✅ Contenedor de UAT creado en puerto 8081"
echo ""

# Configurar Nginx para ambos ambientes
echo "⚙️  Configurando Nginx para ambos ambientes..."

# Backup de configuración anterior si existe
if [ -f /etc/nginx/sites-available/molpi ]; then
    cp /etc/nginx/sites-available/molpi /etc/nginx/sites-available/molpi.backup
fi

cat > /etc/nginx/sites-available/molpi-multi << 'NGINX_MULTI'
# ============================================
# PRODUCCIÓN - molpi.com.ar
# ============================================

# HTTP redirect
server {
    listen 80;
    listen [::]:80;
    server_name molpi.com.ar www.molpi.com.ar;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS - PRODUCCIÓN
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name molpi.com.ar www.molpi.com.ar;
    
    # SSL
    ssl_certificate /etc/letsencrypt/live/molpi.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/molpi.com.ar/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Logs
    access_log /var/log/nginx/molpi_prod_access.log;
    error_log /var/log/nginx/molpi_prod_error.log;
    
    client_max_body_size 20M;
    
    # Proxy a contenedor de PRODUCCIÓN (puerto 8080)
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}

# ============================================
# UAT - uat.molpi.com.ar
# ============================================

# HTTP redirect
server {
    listen 80;
    listen [::]:80;
    server_name uat.molpi.com.ar;
    
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS - UAT
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name uat.molpi.com.ar;
    
    # SSL
    ssl_certificate /etc/letsencrypt/live/molpi.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/molpi.com.ar/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Logs
    access_log /var/log/nginx/molpi_uat_access.log;
    error_log /var/log/nginx/molpi_uat_error.log;
    
    client_max_body_size 20M;
    
    # Banner de UAT
    add_header X-Environment "UAT" always;
    
    # Proxy a contenedor de UAT (puerto 8081)
    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
NGINX_MULTI

# Activar configuración
ln -sf /etc/nginx/sites-available/molpi-multi /etc/nginx/sites-enabled/molpi
rm -f /etc/nginx/sites-enabled/default

# Verificar configuración
nginx -t

echo "✅ Nginx configurado para ambos ambientes"
echo ""

# Recargar Nginx
systemctl reload nginx

echo "======================================================================"
echo "✅ ¡AMBIENTES CONFIGURADOS!"
echo "======================================================================"
echo ""
echo "🏭 PRODUCCIÓN:"
echo "   URL: https://molpi.com.ar"
echo "   Contenedor: molpi-produccion"
echo "   Puerto interno: 8080"
echo "   Datos: /opt/molpi/produccion/data"
echo ""
echo "🧪 UAT:"
echo "   URL: https://uat.molpi.com.ar"
echo "   Contenedor: molpi-uat"
echo "   Puerto interno: 8081"
echo "   Datos: /opt/molpi/uat/data"
echo ""
echo "📊 Ver logs:"
echo "   Producción: docker logs -f molpi-produccion"
echo "   UAT: docker logs -f molpi-uat"
echo ""
echo "🔄 Reiniciar:"
echo "   Producción: docker restart molpi-produccion"
echo "   UAT: docker restart molpi-uat"
echo ""
echo "⚠️  IMPORTANTE: Configura estos registros DNS:"
echo "   molpi.com.ar     A    179.43.112.121"
echo "   www.molpi.com.ar A    179.43.112.121"
echo "   uat.molpi.com.ar A    179.43.112.121"
echo ""
