# 🚨 SOLUCIÓN PARA ERRORES 500 EN PYTHONANYWHERE

## 📊 DIAGNÓSTICO CONFIRMADO
- ✅ Backend funciona (/health = 200)
- ❌ Todas las consultas SQL fallan (500)
- 🎯 Problema: Consultas SQL incompatibles con esquema DB

## 🔧 SOLUCIÓN RÁPIDA

### OPCIÓN 1: Probar URLs de Debug
Accede a estas URLs directamente en tu navegador:

1. **https://sgit.pythonanywhere.com/api/debug/db-info**
   - Mostrará info detallada de la base de datos

2. **https://sgit.pythonanywhere.com/api/debug/test-queries**  
   - Probará las consultas específicas que fallan

3. **https://sgit.pythonanywhere.com/api/debug/raw-categorias**
   - Query más simple para ver qué devuelve

### OPCIÓN 2: Subir App Simplificado (RECOMENDADO)

Crear un `app_simple.py` que use queries más básicas sin columnas problemáticas:

```python
# Endpoints simplificados
@app.route('/api/categorias')
def get_categorias_simple():
    try:
        conn = sqlite3.connect('molpi.db')
        c = conn.cursor()
        
        # Query más simple - solo columnas básicas
        c.execute("SELECT id, nombre FROM categorias")
        rows = c.fetchall()
        
        categorias = []
        for row in rows:
            categorias.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': '',  # Valor por defecto
                'activo': 1         # Valor por defecto
            })
        
        conn.close()
        return jsonify(categorias)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### OPCIÓN 3: Verificar Reload
Si subiste archivos nuevos:

1. **PythonAnywhere Dashboard** → **Web** tab
2. Click **"Reload"** (verde)
3. Esperar "Reloaded successfully"
4. Probar: https://sgit.pythonanywhere.com/api/categorias

## 🎯 PRÓXIMO PASO

**¿Qué prefieres hacer?**

1. **Debug**: Probar las URLs de debug para ver el error exacto
2. **Simple**: Subir version simplificada del backend
3. **Verificar**: Confirmar que hiciste Reload después de subir archivos

**Respuesta rápida:** Escribe "debug", "simple" o "reload"
