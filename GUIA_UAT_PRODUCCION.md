# 🚀 Guía de Ambientes UAT y Producción

## 📋 Estructura de Ambientes

```
Servidor VPS (179.43.112.121)
│
├── 🏭 PRODUCCIÓN
│   ├── URL: https://molpi.com.ar
│   ├── Puerto: 8080
│   ├── Contenedor: molpi-prod
│   ├── BD: /opt/molpi/produccion/data/molpi.db
│   └── Logs: /opt/molpi/produccion/logs/
│
└── 🧪 UAT (Testing)
    ├── URL: https://uat.molpi.com.ar
    ├── Puerto: 8081
    ├── Contenedor: molpi-uat
    ├── BD: /opt/molpi/uat/data/molpi.db (independiente)
    └── Logs: /opt/molpi/uat/logs/
```

---

## 🎯 Configuración Inicial (Solo una vez)

### 1️⃣ Configurar DNS en Cloudflare

Agregar registro para UAT:
- **Type**: A
- **Name**: uat
- **Content**: 179.43.112.121
- **Proxy**: DNS only (gris) temporalmente

### 2️⃣ Ejecutar script de configuración

En el servidor:
```bash
cd /opt/molpi/MolpiOriginal2
chmod +x setup-uat.sh
./setup-uat.sh
```

Esto va a:
- ✅ Crear estructura de directorios separados
- ✅ Mover producción actual a /opt/molpi/produccion/
- ✅ Crear ambiente UAT en /opt/molpi/uat/
- ✅ Configurar Nginx para ambos dominios
- ✅ Obtener certificado SSL para uat.molpi.com.ar

---

## 🔄 Flujo de Trabajo Normal

### **Escenario 1: Cambio de Código (HTML, CSS, JavaScript, Python)**

#### A) Actualizar UAT primero

1. **Editar código en el servidor**:
   ```bash
   cd /opt/molpi/MolpiOriginal2
   nano backend/app.py  # o el archivo que necesites
   ```

2. **Actualizar UAT**:
   ```bash
   ./actualizar-uat.sh
   ```

3. **Probar en UAT**: https://uat.molpi.com.ar
   - Verifica que todo funcione correctamente
   - Prueba todas las funcionalidades nuevas

4. **Si todo está OK, promover a Producción**:
   ```bash
   ./promover-a-prod.sh
   ```

#### B) Promover directamente a Producción (solo código, sin BD)

Si solo cambiaste código y NO cambiaste la base de datos:

```bash
cd /opt/molpi/MolpiOriginal2
docker build -t molpi-app:latest .
docker restart molpi-prod
```

---

### **Escenario 2: Cambios en Base de Datos**

#### Opción A: Probar en UAT primero (Recomendado)

1. **Hacer cambios en UAT**:
   - Agregar/editar productos en https://uat.molpi.com.ar/admin
   - Hacer los cambios que necesites

2. **Verificar que todo está OK**

3. **Promover BD de UAT a Producción**:
   ```bash
   ./promover-a-prod.sh
   ```
   ⚠️ Esto **REEMPLAZA** la BD de producción con la de UAT

#### Opción B: Hacer backup y trabajar directo en Producción

```bash
# Backup manual
docker cp molpi-prod:/app/backend/molpi.db /opt/molpi/produccion/backups/molpi_$(date +%Y%m%d_%H%M%S).db

# Hacer cambios en https://molpi.com.ar/admin
```

---

## 📊 Comandos Útiles

### Ver estado de los contenedores
```bash
docker ps
```

### Ver logs en tiempo real
```bash
# Producción
docker logs -f molpi-prod

# UAT
docker logs -f molpi-uat
```

### Reiniciar ambientes
```bash
# Producción
docker restart molpi-prod

# UAT
docker restart molpi-uat
```

### Ver uso de recursos
```bash
docker stats molpi-prod molpi-uat
```

### Acceder a un contenedor
```bash
# Producción
docker exec -it molpi-prod bash

# UAT
docker exec -it molpi-uat bash
```

---

## 💾 Gestión de Backups

### Backup manual de Producción
```bash
docker cp molpi-prod:/app/backend/molpi.db /opt/molpi/produccion/backups/molpi_$(date +%Y%m%d_%H%M%S).db
```

### Backup manual de UAT
```bash
docker cp molpi-uat:/app/backend/molpi.db /opt/molpi/uat/backups/molpi_$(date +%Y%m%d_%H%M%S).db
```

### Restaurar backup en Producción
```bash
docker stop molpi-prod
cp /opt/molpi/produccion/backups/molpi_YYYYMMDD_HHMMSS.db /opt/molpi/produccion/data/molpi.db
docker start molpi-prod
```

### Listar backups disponibles
```bash
ls -lh /opt/molpi/produccion/backups/
ls -lh /opt/molpi/uat/backups/
```

---

## 🔙 Revertir Cambios

### Si algo sale mal después de promoción

```bash
# 1. Ver backups disponibles
ls -lh /opt/molpi/produccion/backups/

# 2. Restaurar el backup pre-promoción
docker stop molpi-prod
cp /opt/molpi/produccion/backups/molpi_pre_promocion_TIMESTAMP.db /opt/molpi/produccion/data/molpi.db
docker start molpi-prod
```

---

## 🎨 Diferencias entre UAT y Producción

| Característica | Producción | UAT |
|---------------|------------|-----|
| URL | molpi.com.ar | uat.molpi.com.ar |
| Puerto | 8080 | 8081 |
| Base de datos | Independiente | Independiente |
| FLASK_ENV | production | development |
| Usuarios | Clientes reales | Solo testing |
| SSL | ✅ | ✅ |

---

## 🔄 Workflows Comunes

### Workflow 1: Agregar nuevo producto

```bash
# 1. Agregar en UAT
# Ve a: https://uat.molpi.com.ar/admin
# Agregar producto con imágenes

# 2. Verificar que se vea bien en UAT
# https://uat.molpi.com.ar

# 3. Promover a producción
./promover-a-prod.sh

# 4. Verificar en producción
# https://molpi.com.ar
```

### Workflow 2: Cambio visual (CSS/HTML)

```bash
# 1. Editar archivo
nano /opt/molpi/MolpiOriginal2/www.molpi.com.ar/css/custom.css

# 2. Actualizar UAT
./actualizar-uat.sh

# 3. Verificar en https://uat.molpi.com.ar

# 4. Si está OK, actualizar producción
docker build -t molpi-app:latest .
docker stop molpi-prod
docker rm molpi-prod
docker run -d --name molpi-prod --restart unless-stopped -p 127.0.0.1:8080:8080 -v /opt/molpi/produccion/data:/app/backend/data -v /opt/molpi/produccion/logs:/app/logs -e FLASK_ENV=production molpi-app:latest
```

### Workflow 3: Cambio en backend (Python)

```bash
# 1. Editar código
nano /opt/molpi/MolpiOriginal2/backend/app.py

# 2. Actualizar UAT
./actualizar-uat.sh

# 3. Probar API en UAT
curl https://uat.molpi.com.ar/api/productos

# 4. Si funciona, actualizar producción
docker build -t molpi-app:latest .
docker restart molpi-prod
```

---

## 🚨 Troubleshooting

### UAT no responde
```bash
# Ver logs
docker logs molpi-uat --tail 50

# Reiniciar
docker restart molpi-uat

# Si sigue sin funcionar, recrear
docker stop molpi-uat
docker rm molpi-uat
./setup-uat.sh
```

### Producción no responde
```bash
# Ver logs
docker logs molpi-prod --tail 50

# Reiniciar
docker restart molpi-prod

# Verificar Nginx
systemctl status nginx
nginx -t
```

### Problemas de SSL
```bash
# Ver certificados
certbot certificates

# Renovar manualmente
certbot renew

# Reiniciar Nginx
systemctl reload nginx
```

### Base de datos corrupta
```bash
# Restaurar desde backup
docker stop molpi-prod
cp /opt/molpi/produccion/backups/molpi_YYYYMMDD.db /opt/molpi/produccion/data/molpi.db
docker start molpi-prod
```

---

## 📝 Scripts Disponibles

| Script | Descripción | Cuándo usarlo |
|--------|-------------|---------------|
| `setup-uat.sh` | Configuración inicial de UAT | Solo la primera vez |
| `actualizar-uat.sh` | Actualizar código en UAT | Cada vez que cambies código |
| `promover-a-prod.sh` | Copiar UAT a Producción | Cuando UAT esté OK |
| `setup-ssl.sh` | Configurar SSL | Ya está configurado |
| `update-prod.sh` | Actualizar solo producción | Para hotfixes urgentes |

---

## 🎯 Recomendaciones

1. **Siempre probar en UAT primero** antes de tocar producción
2. **Hacer backup** antes de cualquier cambio importante
3. **Ver los logs** si algo no funciona
4. **Documentar** los cambios que haces
5. **Mantener backups** de al menos 30 días

---

## 🔐 Credenciales

**Admin (ambos ambientes):**
- Usuario: admin
- Contraseña: dumba3110

**Servidor VPS:**
- Host: 179.43.112.121
- Puerto SSH: 5690
- Usuario: root
- Contraseña: aN)-2y87mdRiut

---

## 📞 Ayuda Rápida

```bash
# Ver todo el estado del sistema
docker ps
systemctl status nginx
df -h

# Reiniciar todo
docker restart molpi-prod molpi-uat
systemctl restart nginx

# Logs en vivo
docker logs -f molpi-prod
docker logs -f molpi-uat
tail -f /var/log/nginx/error.log
```
