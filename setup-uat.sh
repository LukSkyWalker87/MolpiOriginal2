#!/bin/bash
# Script para configurar ambiente UAT

set -e

echo "======================================================================"
echo "🧪 CONFIGURACIÓN DE AMBIENTE UAT"
echo "======================================================================"
echo ""

# 1. Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p /opt/molpi/produccion/data
mkdir -p /opt/molpi/produccion/logs
mkdir -p /opt/molpi/produccion/backups
mkdir -p /opt/molpi/uat/data
mkdir -p /opt/molpi/uat/logs
mkdir -p /opt/molpi/uat/backups
echo "✅ Directorios creados"
echo ""

# 2. Mover contenedor actual a producción
echo "🔄 Configurando ambiente de PRODUCCIÓN..."
docker stop molpi-prod 2>/dev/null || true
docker rm molpi-prod 2>/dev/null || true

# Copiar BD actual a producción si no existe
if [ ! -f /opt/molpi/produccion/data/molpi.db ]; then
    if [ -f /opt/molpi/data/molpi.db ]; then
        echo "📋 Copiando BD existente a producción..."
        cp /opt/molpi/data/molpi.db /opt/molpi/produccion/data/molpi.db
    else
        echo "📋 Copiando BD desde código fuente..."
        cp /opt/molpi/MolpiOriginal2/backend/molpi.db /opt/molpi/produccion/data/molpi.db
    fi
fi

# Crear contenedor de producción
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v /opt/molpi/produccion/data:/app/backend/data \
  -v /opt/molpi/produccion/logs:/app/logs \
  -e FLASK_ENV=production \
  -e ENVIRONMENT=production \
  molpi-app:latest

echo "✅ Contenedor de PRODUCCIÓN creado"
echo ""

# 3. Crear ambiente UAT
echo "🧪 Configurando ambiente de UAT..."

# Copiar BD de producción a UAT
cp /opt/molpi/produccion/data/molpi.db /opt/molpi/uat/data/molpi.db

# Crear contenedor de UAT
docker run -d \
  --name molpi-uat \
  --restart unless-stopped \
  -p 127.0.0.1:8081:8080 \
  -v /opt/molpi/uat/data:/app/backend/data \
  -v /opt/molpi/uat/logs:/app/logs \
  -e FLASK_ENV=development \
  -e ENVIRONMENT=uat \
  molpi-app:latest

echo "✅ Contenedor de UAT creado"
echo ""

# 4. Configurar Nginx para ambos ambientes
echo "⚙️  Configurando Nginx..."

cat > /etc/nginx/sites-available/molpi << 'NGINX_CONFIG'
# ============================================
# PRODUCCIÓN - molpi.com.ar
# ============================================
server {
    listen 80;
    listen [::]:80;
    server_name molpi.com.ar www.molpi.com.ar;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name molpi.com.ar www.molpi.com.ar;
    
    ssl_certificate /etc/letsencrypt/live/molpi.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/molpi.com.ar/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    access_log /var/log/nginx/molpi_prod_access.log;
    error_log /var/log/nginx/molpi_prod_error.log;
    
    client_max_body_size 20M;
    
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
server {
    listen 80;
    listen [::]:80;
    server_name uat.molpi.com.ar;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name uat.molpi.com.ar;
    
    ssl_certificate /etc/letsencrypt/live/molpi.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/molpi.com.ar/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    access_log /var/log/nginx/molpi_uat_access.log;
    error_log /var/log/nginx/molpi_uat_error.log;
    
    client_max_body_size 20M;
    
    # Banner de UAT
    add_header X-Environment "UAT" always;
    
    location / {
        proxy_pass http://127.0.0.1:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
NGINX_CONFIG

nginx -t
systemctl reload nginx

echo "✅ Nginx configurado"
echo ""

# 5. Obtener certificado SSL para UAT
echo "🔐 Configurando SSL para UAT..."
certbot certonly --nginx -d uat.molpi.com.ar --non-interactive --agree-tos --email contacto@molpi.com.ar 2>/dev/null || echo "⚠️  Certificado ya existe o dominio no resuelve aún"
systemctl reload nginx
echo ""

echo "======================================================================"
echo "✅ ¡AMBIENTES CONFIGURADOS!"
echo "======================================================================"
echo ""
echo "🏭 PRODUCCIÓN:"
echo "   URL: https://molpi.com.ar"
echo "   Contenedor: molpi-prod"
echo "   Puerto: 8080"
echo "   BD: /opt/molpi/produccion/data/molpi.db"
echo ""
echo "🧪 UAT:"
echo "   URL: https://uat.molpi.com.ar"
echo "   Contenedor: molpi-uat"
echo "   Puerto: 8081"
echo "   BD: /opt/molpi/uat/data/molpi.db"
echo ""
echo "📊 Ver logs:"
echo "   docker logs -f molpi-prod"
echo "   docker logs -f molpi-uat"
echo ""
echo "🔄 Para promover UAT a Producción:"
echo "   /opt/molpi/MolpiOriginal2/promover-a-prod.sh"
echo ""
