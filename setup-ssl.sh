#!/bin/bash
# Script para configurar SSL y Nginx en VPS

set -e

echo "======================================================================"
echo "🔒 CONFIGURACIÓN SSL PARA MOLPI"
echo "======================================================================"
echo ""

# Paso 1: Instalar Nginx
echo "📦 Paso 1/6: Instalando Nginx..."
apt-get update
apt-get install -y nginx
systemctl enable nginx
echo "✅ Nginx instalado"
echo ""

# Paso 2: Instalar Certbot
echo "📦 Paso 2/6: Instalando Certbot para SSL..."
apt-get install -y certbot python3-certbot-nginx
echo "✅ Certbot instalado"
echo ""

# Paso 3: Detener Nginx temporalmente
echo "🛑 Paso 3/6: Deteniendo Nginx temporalmente..."
systemctl stop nginx
echo "✅ Nginx detenido"
echo ""

# Paso 4: Reconfigurar contenedor Docker
echo "🔄 Paso 4/6: Reconfigurando contenedor para usar solo localhost..."
docker stop molpi-prod
docker rm molpi-prod
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v /opt/molpi/data:/app/backend/data \
  -v /opt/molpi/logs:/app/logs \
  -e FLASK_ENV=production \
  molpi-app:latest
echo "✅ Contenedor reconfigurado"
echo ""

# Paso 5: Configurar Nginx
echo "⚙️  Paso 5/6: Configurando Nginx..."
cat > /etc/nginx/sites-available/molpi << 'NGINX_CONFIG'
# Configuración HTTP (redirige a HTTPS)
server {
    listen 80;
    listen [::]:80;
    server_name molpi.com.ar www.molpi.com.ar;
    
    # Permitir certbot
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    # Redirigir todo a HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# Configuración HTTPS
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name molpi.com.ar www.molpi.com.ar;
    
    # Certificados SSL (se configurarán con certbot)
    ssl_certificate /etc/letsencrypt/live/molpi.com.ar/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/molpi.com.ar/privkey.pem;
    
    # Configuración SSL moderna
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Logs
    access_log /var/log/nginx/molpi_access.log;
    error_log /var/log/nginx/molpi_error.log;
    
    # Tamaño máximo de archivos
    client_max_body_size 20M;
    
    # Proxy a la aplicación Docker
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Cache para archivos estáticos
    location /static/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_cache_valid 200 1d;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
NGINX_CONFIG

# Activar configuración
ln -sf /etc/nginx/sites-available/molpi /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Verificar configuración
nginx -t
echo "✅ Nginx configurado"
echo ""

# Paso 6: Obtener certificado SSL
echo "🔐 Paso 6/6: Obteniendo certificado SSL..."
echo ""
echo "⚠️  IMPORTANTE: Asegúrate de que el dominio molpi.com.ar apunte a:"
echo "   IP: 179.43.112.121"
echo ""
read -p "¿El dominio ya está apuntando a esta IP? (s/n): " respuesta

if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
    certbot certonly --nginx -d molpi.com.ar -d www.molpi.com.ar --non-interactive --agree-tos --email contacto@molpi.com.ar
    
    # Iniciar Nginx
    systemctl start nginx
    systemctl reload nginx
    
    echo ""
    echo "======================================================================"
    echo "✅ ¡SSL CONFIGURADO EXITOSAMENTE!"
    echo "======================================================================"
    echo ""
    echo "🌐 Tu aplicación está disponible en:"
    echo "   https://molpi.com.ar"
    echo "   https://www.molpi.com.ar"
    echo ""
    echo "🔄 Auto-renovación de certificado configurada"
    echo ""
else
    echo ""
    echo "⚠️  Por favor configura el dominio primero:"
    echo "   1. Ve a tu panel de DNS"
    echo "   2. Crea un registro A para molpi.com.ar apuntando a 179.43.112.121"
    echo "   3. Crea un registro A para www.molpi.com.ar apuntando a 179.43.112.121"
    echo "   4. Espera 5-10 minutos para que se propague"
    echo "   5. Ejecuta este script nuevamente"
    echo ""
    
    # Configuración temporal sin SSL
    cat > /etc/nginx/sites-available/molpi << 'NGINX_TEMP'
server {
    listen 80;
    listen [::]:80;
    server_name molpi.com.ar www.molpi.com.ar _;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_TEMP
    
    systemctl start nginx
    
    echo "✅ Nginx configurado temporalmente sin SSL"
    echo "🌐 Aplicación accesible en: http://179.43.112.121"
fi
