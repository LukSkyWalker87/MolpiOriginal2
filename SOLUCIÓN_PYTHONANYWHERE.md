# 🚀 SOLUCIÓN PARA MOLPI ADMIN - PythonAnywhere

## 📋 DIAGNÓSTICO
- ✅ **Local**: DB funciona (112 productos, 7 categorías)
- ✅ **Frontend**: Admin carga con categorías por defecto
- ❌ **PythonAnywhere**: Backend da 500 en /api/categorias y /api/productos

## 🎯 SOLUCIÓN: SUBIR DB Y BACKEND ACTUALIZADOS

### PASO 1: Subir Base de Datos
1. **Ubicar archivo local**: `Python/molpi.db` (108 KB)
2. **Conectar por FTP/Files a PythonAnywhere**
3. **Subir a**: `/home/sgit/mysite/molpi.db` (reemplazar la actual)
4. **Verificar tamaño**: Debe ser ~108 KB (no 4 KB como antes)

### PASO 2: Subir Backend Actualizado  
1. **Subir archivo**: `Python/app.py` actualizado
2. **Ubicación destino**: `/home/sgit/mysite/app.py`
3. **Hacer Reload** de la aplicación web en PythonAnywhere

### PASO 3: Verificar Funcionamiento
1. **Probar**: https://sgit.pythonanywhere.com/api/health
2. **Debe responder**: `{"status": "healthy", "message": "API funcionando correctamente"}`
3. **Probar**: https://sgit.pythonanywhere.com/api/categorias
4. **Debe responder**: Lista de 7 categorías
5. **Probar**: https://sgit.pythonanywhere.com/api/productos
6. **Debe responder**: Lista de productos (112 elementos)

### PASO 4: Verificar Admin
1. **Refrescar Vercel**: Ctrl+F5 en https://molpi-admin.vercel.app/admin.html
2. **Debe mostrar**: 
   - Categorías funcionando ✅
   - Productos cargando ✅
   - Sin errores 500 ✅

## 🔧 ARCHIVOS IMPORTANTES

### Base de Datos Actual (Local)
```
Archivo: Python/molpi.db (108.0 KB)
Tablas: 7 
├── productos: 112 registros, 13 columnas
├── categorias: 7 registros, 4 columnas  
├── subcategorias: 1301 registros, 5 columnas
├── promociones: 2 registros, 10 columnas
├── testimonios: 5 registros, 9 columnas
├── producto_imagenes: 0 registros, 4 columnas
└── sqlite_sequence: 5 registros, 2 columnas
```

### Backend Actualizado
- **Archivo**: `Python/app.py`
- **Incluye**: 
  - Migraciones defensivas automáticas
  - Endpoints /api/* funcionando
  - Manejo de errores robusto
  - CORS configurado

## ⚡ RESULTADO ESPERADO
Después de subir ambos archivos:
- ✅ https://sgit.pythonanywhere.com/api/categorias → 200 OK
- ✅ https://sgit.pythonanywhere.com/api/productos → 200 OK  
- ✅ Admin en Vercel mostrará productos reales
- ✅ Filtros por categoría funcionando
- ✅ Sin errores 500 ni 404

## 🚨 IMPORTANTE
- **NO cambiar nombres** de archivos
- **Hacer backup** de archivos actuales en PythonAnywhere antes de reemplazar
- **Reload aplicación** después de subir app.py
- **Verificar URLs** antes de declarar éxito

La base de datos local ya tiene todos los datos correctos (112 productos). 
Solo necesitas subirla a PythonAnywhere para que funcione en producción.
