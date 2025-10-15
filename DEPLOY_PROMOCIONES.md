# Pasos para Deploy de Promociones

## Contexto
Las promociones se guardan correctamente en la base de datos, pero el componente en el servidor no se actualiza debido a caché de Docker.

## Pasos en el Servidor

```bash
# 1. Navegar al directorio del proyecto
cd /opt/molpi/MolpiOriginal2

# 2. Obtener los últimos cambios desde GitHub
git pull origin main

# 3. Detener todos los contenedores
docker compose down

# 4. Eliminar la imagen vieja para forzar reconstrucción completa
docker rmi molpioriginal2-molpi-app

# 5. Reconstruir SIN caché (importante para refrescar archivos estáticos)
docker compose build --no-cache

# 6. Levantar los contenedores
docker compose up -d

# 7. Verificar que el archivo está actualizado dentro del contenedor
docker exec -it molpioriginal2-molpi-app-1 cat /app/www.molpi.com.ar/components/promociones.html | grep "🟢🟢🟢 SCRIPT DE PROMOCIONES CARGADO"

# Deberías ver: console.log('🟢🟢🟢 SCRIPT DE PROMOCIONES CARGADO! 🟢🟢🟢');

# 8. Ver logs del contenedor para verificar que inició correctamente
docker compose logs -f molpi-app

# 9. Reiniciar nginx del host (para limpiar cualquier caché)
sudo systemctl restart nginx

# 10. Verificar que nginx está corriendo
sudo systemctl status nginx
```

## Verificación en el Navegador

1. Abrir el navegador en modo incógnito (Ctrl+Shift+N en Chrome)
2. Ir a https://www.molpi.com.ar/admin
3. Iniciar sesión
4. Ir a la sección "Promociones"
5. Abrir la consola del navegador (F12)
6. Deberías ver: `🟢🟢🟢 SCRIPT DE PROMOCIONES CARGADO! 🟢🟢🟢`
7. Deberías ver: `🔵 Inicializando promociones...`
8. Deberías ver: `🔵 cargarPromociones() llamada`
9. La tabla debería mostrar las 2 promociones existentes

## Solución de Problemas

### Si el archivo no se actualiza dentro del contenedor:
```bash
# Forzar eliminación de volúmenes
docker compose down -v

# Limpiar sistema Docker completo
docker system prune -af

# Reconstruir desde cero
docker compose build --no-cache
docker compose up -d
```

### Si aún no funciona:
```bash
# Verificar que el archivo existe en el host
ls -la /opt/molpi/MolpiOriginal2/www.molpi.com.ar/components/promociones.html

# Ver la fecha de modificación (debe ser reciente)
stat /opt/molpi/MolpiOriginal2/www.molpi.com.ar/components/promociones.html

# Verificar el contenido
head -n 230 /opt/molpi/MolpiOriginal2/www.molpi.com.ar/components/promociones.html | tail -n 10
```

### Si nginx tiene caché:
```bash
# Limpiar caché de nginx
sudo rm -rf /var/cache/nginx/*
sudo systemctl restart nginx
```

## Commit Actual
El último commit con los cambios es: `0c408d3`
Mensaje: "Debug: Agregar logs a cargarPromociones y renderPromocionRow"

## Archivos Modificados
- `www.molpi.com.ar/components/promociones.html` - Componente de promociones con logs de debugging
- `backend/app.py` - Endpoint `/upload/promocion` agregado
- `www.molpi.com.ar/admin.html` - Carga dinámica de componentes

## Verificación Final
Después del deploy, las promociones deberían:
1. ✅ Guardarse en la base de datos (ya funciona)
2. ✅ Mostrarse en la tabla del admin con botones Editar/Eliminar
3. ✅ Mostrarse en index.html si están activas (activo=1)
