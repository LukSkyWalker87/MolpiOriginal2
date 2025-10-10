# 🚀 Guía de Configuración - SSL y Ambientes UAT/Producción

## 📋 Requisitos Previos

1. **Configurar DNS** (IMPORTANTE - Hacer ANTES de configurar SSL):
   - Ve a tu panel de DNS (donde administras molpi.com.ar)
   - Crea estos registros A:
     ```
     molpi.com.ar     → 179.43.112.121
     www.molpi.com.ar → 179.43.112.121
     uat.molpi.com.ar → 179.43.112.121
     ```
   - Espera 5-10 minutos para que se propague

2. **Verificar DNS** desde tu PC:
   ```powershell
   nslookup molpi.com.ar
   nslookup uat.molpi.com.ar
   ```

---

## 🔒 PASO 1: Configurar SSL

En el servidor VPS, ejecuta:

```bash
cd /opt/molpi/MolpiOriginal2
chmod +x setup-ssl.sh
./setup-ssl.sh
```

Este script:
- ✅ Instala Nginx
- ✅ Instala Certbot (Let's Encrypt)
- ✅ Reconfigura el contenedor Docker
- ✅ Obtiene certificado SSL gratuito
- ✅ Configura auto-renovación

**Resultado:**
- 🌐 https://molpi.com.ar funcionando con SSL

---

## 🔄 PASO 2: Configurar Ambientes UAT y Producción

En el servidor VPS, ejecuta:

```bash
cd /opt/molpi/MolpiOriginal2
chmod +x setup-ambientes.sh
./setup-ambientes.sh
```

Este script:
- ✅ Crea estructura de directorios separados
- ✅ Crea contenedor de PRODUCCIÓN (puerto 8080)
- ✅ Crea contenedor de UAT (puerto 8081)
- ✅ Configura Nginx para ambos ambientes

**Resultado:**
- 🏭 **Producción**: https://molpi.com.ar
- 🧪 **UAT**: https://uat.molpi.com.ar

---

## 📁 Estructura de Directorios

```
/opt/molpi/
├── MolpiOriginal2/          # Código fuente
├── produccion/
│   ├── data/                # BD de producción
│   ├── logs/                # Logs de producción
│   └── backups/             # Backups automáticos
└── uat/
    ├── data/                # BD de UAT (independiente)
    ├── logs/                # Logs de UAT
    └── backups/             # Backups de UAT
```

---

## 🔄 Flujo de Trabajo para Deployments

### Opción A: Deploy a UAT (Testing)

```bash
cd /opt/molpi/MolpiOriginal2
chmod +x deploy-uat.sh
./deploy-uat.sh
```

**Pasos que ejecuta:**
1. Actualiza código desde GitHub
2. Construye nueva imagen
3. Reinicia contenedor de UAT
4. Verifica que funcione

**Testing:** https://uat.molpi.com.ar

---

### Opción B: Deploy a Producción (Cliente)

⚠️ **Solo después de probar en UAT**

```bash
cd /opt/molpi/MolpiOriginal2
chmod +x deploy-prod.sh
./deploy-prod.sh
```

**Pasos que ejecuta:**
1. Crea backup automático de la BD
2. Actualiza código desde GitHub
3. Construye nueva imagen
4. Reinicia contenedor de producción
5. Verifica que funcione

**Live:** https://molpi.com.ar

---

## 📊 Comandos Útiles

### Ver logs en tiempo real
```bash
# Producción
docker logs -f molpi-produccion

# UAT
docker logs -f molpi-uat
```

### Ver estado de contenedores
```bash
docker ps
```

### Reiniciar aplicaciones
```bash
# Producción
docker restart molpi-produccion

# UAT
docker restart molpi-uat
```

### Acceder al contenedor
```bash
# Producción
docker exec -it molpi-produccion bash

# UAT
docker exec -it molpi-uat bash
```

### Ver uso de recursos
```bash
docker stats
```

---

## 💾 Backups

### Backup Manual

**Producción:**
```bash
docker cp molpi-produccion:/app/backend/molpi.db /opt/molpi/produccion/backups/molpi_$(date +%Y%m%d_%H%M%S).db
```

**UAT:**
```bash
docker cp molpi-uat:/app/backend/molpi.db /opt/molpi/uat/backups/molpi_$(date +%Y%m%d_%H%M%S).db
```

### Restaurar Backup

```bash
# 1. Detener contenedor
docker stop molpi-produccion

# 2. Copiar backup
cp /opt/molpi/produccion/backups/molpi_FECHA.db /opt/molpi/produccion/data/molpi.db

# 3. Iniciar contenedor
docker start molpi-produccion
```

---

## 🔧 Troubleshooting

### SSL no funciona
```bash
# Verificar certificados
certbot certificates

# Renovar manualmente
certbot renew

# Ver logs de Nginx
tail -f /var/log/nginx/error.log
```

### Aplicación no responde
```bash
# Ver logs
docker logs molpi-produccion

# Reiniciar
docker restart molpi-produccion

# Verificar Nginx
systemctl status nginx
nginx -t
```

### Problemas de DNS
```bash
# Verificar que apunte correctamente
nslookup molpi.com.ar
dig molpi.com.ar

# Verificar desde el servidor
curl -I https://molpi.com.ar
```

---

## 📅 Mantenimiento Automático

### Auto-renovación de SSL
Certbot configura automáticamente un cron job para renovar certificados.

Verificar:
```bash
systemctl status certbot.timer
```

### Backup Automático Diario

Crear cron job:
```bash
crontab -e
```

Agregar:
```bash
# Backup diario a las 2 AM
0 2 * * * docker cp molpi-produccion:/app/backend/molpi.db /opt/molpi/produccion/backups/molpi_$(date +\%Y\%m\%d).db

# Limpiar backups antiguos (más de 30 días)
0 3 * * * find /opt/molpi/produccion/backups -name "molpi_*.db" -mtime +30 -delete
```

---

## 🎯 Resumen de URLs

| Ambiente | URL | Contenedor | Puerto |
|----------|-----|------------|--------|
| Producción | https://molpi.com.ar | molpi-produccion | 8080 |
| UAT | https://uat.molpi.com.ar | molpi-uat | 8081 |

---

## ✅ Checklist de Setup

- [ ] Configurar registros DNS
- [ ] Verificar propagación DNS
- [ ] Ejecutar `setup-ssl.sh`
- [ ] Verificar SSL en https://molpi.com.ar
- [ ] Ejecutar `setup-ambientes.sh`
- [ ] Verificar UAT en https://uat.molpi.com.ar
- [ ] Probar deploy en UAT con `deploy-uat.sh`
- [ ] Probar deploy en Producción con `deploy-prod.sh`
- [ ] Configurar backups automáticos
- [ ] Documentar credenciales de acceso

---

## 📞 Soporte

Para problemas o dudas:
1. Revisar logs: `docker logs -f molpi-produccion`
2. Verificar Nginx: `nginx -t && systemctl status nginx`
3. Verificar DNS: `nslookup molpi.com.ar`
