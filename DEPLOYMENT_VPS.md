# Guía de Deployment - VPS Docker Ubuntu 24.04

## 📋 Información del Servidor

- **Host**: vps-5346672-x.dattaweb.com
- **IP**: 179.43.112.121
- **Usuario**: root
- **Puerto SSH**: 5690
- **Sistema**: Ubuntu 24.04 con Docker

## 🚀 Opción 1: Deployment Automático (Recomendado)

### Desde tu PC Windows (PowerShell):

```powershell
# 1. Subir script de deployment al servidor
scp -P 5690 deploy-vps.sh root@179.43.112.121:/tmp/

# 2. Conectar al servidor
ssh -p 5690 root@179.43.112.121

# 3. Ejecutar script (ya en el servidor)
chmod +x /tmp/deploy-vps.sh
/tmp/deploy-vps.sh
```

## 🔧 Opción 2: Deployment Manual

### 1. Conectar al servidor
```bash
ssh -p 5690 root@179.43.112.121
```

### 2. Instalar dependencias
```bash
apt-get update
apt-get install -y git curl
```

### 3. Clonar repositorio
```bash
mkdir -p /opt/molpi
cd /opt/molpi
git clone https://github.com/LukSkyWalker87/MolpiOriginal2.git
cd MolpiOriginal2
```

### 4. Build de la imagen Docker
```bash
docker build -t molpi-app:latest .
```

### 5. Ejecutar contenedor
```bash
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v /opt/molpi/data:/app/backend/data \
  molpi-app:latest
```

## 🌐 Acceso a la Aplicación

Una vez desplegada, tu aplicación estará disponible en:

- **Por IP**: http://179.43.112.121
- **Por Hostname**: http://vps-5346672-x.dattaweb.com

## 📊 Comandos Útiles

### Ver logs en tiempo real
```bash
docker logs -f molpi-prod
```

### Reiniciar aplicación
```bash
docker restart molpi-prod
```

### Detener aplicación
```bash
docker stop molpi-prod
```

### Ver estado del contenedor
```bash
docker ps
```

### Acceder al contenedor
```bash
docker exec -it molpi-prod bash
```

### Ver uso de recursos
```bash
docker stats molpi-prod
```

## 🔄 Actualizar la Aplicación

```bash
# 1. Ir al directorio
cd /opt/molpi/MolpiOriginal2

# 2. Actualizar código
git pull

# 3. Rebuild imagen
docker build -t molpi-app:latest .

# 4. Recrear contenedor
docker stop molpi-prod
docker rm molpi-prod
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 80:5000 \
  -v /opt/molpi/data:/app/backend/data \
  molpi-app:latest
```

## 💾 Backup de la Base de Datos

### Crear backup
```bash
# Copiar desde el contenedor
docker cp molpi-prod:/app/backend/molpi.db /opt/molpi/backups/molpi_$(date +%Y%m%d_%H%M%S).db

# O usar el volumen
cp /opt/molpi/data/molpi.db /opt/molpi/backups/molpi_$(date +%Y%m%d_%H%M%S).db
```

### Restaurar backup
```bash
# Detener contenedor
docker stop molpi-prod

# Restaurar archivo
cp /opt/molpi/backups/molpi_YYYYMMDD_HHMMSS.db /opt/molpi/data/molpi.db

# Iniciar contenedor
docker start molpi-prod
```

## 🔒 Configurar HTTPS con Let's Encrypt (Opcional)

### 1. Instalar Certbot
```bash
apt-get install -y certbot
```

### 2. Obtener certificado
```bash
# Detener la aplicación temporalmente
docker stop molpi-prod

# Obtener certificado
certbot certonly --standalone -d vps-5346672-x.dattaweb.com

# Reiniciar aplicación
docker start molpi-prod
```

### 3. Configurar Nginx como proxy (recomendado para HTTPS)
```bash
apt-get install -y nginx

# Crear configuración
cat > /etc/nginx/sites-available/molpi << 'EOF'
server {
    listen 80;
    server_name vps-5346672-x.dattaweb.com 179.43.112.121;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Activar configuración
ln -s /etc/nginx/sites-available/molpi /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# Ahora modificar el contenedor para no exponer puerto 80
docker stop molpi-prod
docker rm molpi-prod
docker run -d \
  --name molpi-prod \
  --restart unless-stopped \
  -p 127.0.0.1:5000:5000 \
  -v /opt/molpi/data:/app/backend/data \
  molpi-app:latest
```

## 🔥 Firewall (Opcional pero Recomendado)

```bash
# Instalar UFW
apt-get install -y ufw

# Configurar reglas
ufw allow 5690/tcp  # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS

# Activar firewall
ufw --force enable
```

## 🐛 Troubleshooting

### Aplicación no responde
```bash
# Ver logs
docker logs molpi-prod

# Verificar estado
docker ps -a

# Reiniciar
docker restart molpi-prod
```

### Puerto ocupado
```bash
# Ver qué está usando el puerto
netstat -tulpn | grep :80

# Matar proceso si es necesario
kill -9 <PID>
```

### Contenedor no inicia
```bash
# Ver error específico
docker logs molpi-prod

# Verificar imagen
docker images | grep molpi

# Rebuild si es necesario
docker build -t molpi-app:latest .
```

## 📝 Mantenimiento

### Limpieza de Docker
```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune

# Limpieza completa
docker system prune -a
```

### Actualizar sistema
```bash
apt-get update
apt-get upgrade -y
apt-get autoremove -y
```

### Monitoreo de recursos
```bash
# CPU y RAM
htop

# Espacio en disco
df -h

# Docker stats
docker stats
```

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `docker logs -f molpi-prod`
2. Verifica el estado: `docker ps -a`
3. Revisa la conectividad: `curl http://localhost:5000`
