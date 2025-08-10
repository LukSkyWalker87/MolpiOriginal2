#!/usr/bin/env python3
"""
Script para verificar y migrar la base de datos local para que funcione en producción.
Ejecutar desde el directorio raíz del proyecto: python verificar_y_migrar_db.py
"""

import sqlite3
import os
import sys
import json
from datetime import datetime

# Agregar el directorio Python al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Python'))

def verificar_db_local():
    """Verificar el estado de la base de datos local"""
    db_path = os.path.join('Python', 'molpi.db')
    
    print("🔍 VERIFICANDO BASE DE DATOS LOCAL...")
    print(f"Ruta DB: {db_path}")
    print(f"Existe: {'✅ SÍ' if os.path.exists(db_path) else '❌ NO'}")
    
    if not os.path.exists(db_path):
        print("❌ Base de datos local no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Verificar tablas
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = [row[0] for row in c.fetchall()]
        print(f"\n📋 Tablas encontradas: {', '.join(tablas)}")
        
        # Verificar esquema de cada tabla importante
        tablas_importantes = ['productos', 'categorias', 'subcategorias', 'promociones', 'testimonios']
        
        for tabla in tablas_importantes:
            if tabla in tablas:
                c.execute(f"PRAGMA table_info({tabla})")
                columnas = [row[1] for row in c.fetchall()]
                print(f"  📝 {tabla}: {', '.join(columnas)}")
                
                # Contar registros
                c.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = c.fetchone()[0]
                print(f"     📊 {count} registros")
            else:
                print(f"  ❌ {tabla}: NO EXISTE")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando DB: {e}")
        return False

def crear_db_completa():
    """Crear una base de datos completa con el esquema correcto"""
    print("\n🏗️  CREANDO BASE DE DATOS COMPLETA...")
    
    # Importar y ejecutar init_db desde app.py
    try:
        from app import init_db, DB_PATH
        print(f"Creando DB en: {DB_PATH}")
        init_db()
        print("✅ Base de datos creada exitosamente")
        
        # Verificar que se creó correctamente
        return verificar_db_local()
        
    except Exception as e:
        print(f"❌ Error creando DB: {e}")
        return False

def insertar_datos_ejemplo():
    """Insertar algunos datos de ejemplo para testing"""
    print("\n📦 INSERTANDO DATOS DE EJEMPLO...")
    
    db_path = os.path.join('Python', 'molpi.db')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Insertar productos de ejemplo
        productos_ejemplo = [
            ('Molde Baldosa Lisa 40x40', 'Molde para baldosa lisa de 40x40 cm', 'Pisos y Zócalos', 'Línea 40x40', 
             '', 'img/productos/baldosa_40x40.jpg', 'img/mosaicos/baldosa_40x40_mosaic.jpg', 15000.0, 50.0, 1),
            ('Molde Revestimiento Piedra', 'Molde para revestimiento símil piedra', 'Revestimientos', 'Revestimientos Piedra', 
             '', 'img/productos/revestimiento_piedra.jpg', '', 18000.0, 60.0, 1),
            ('Molde Podotáctil Líneas', 'Molde para baldosa podotáctil con líneas', 'Podotáctiles - Discapacidad', 'Señalización', 
             '', 'img/productos/podotactil_lineas.jpg', '', 12000.0, 40.0, 1),
        ]
        
        for producto in productos_ejemplo:
            c.execute("""
                INSERT OR IGNORE INTO productos 
                (nombre, descripcion, categoria, subcategoria, pdf_url, imagen_url, imagen_mosaico_url, precio, precio_usd, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, producto)
        
        # Insertar testimonios de ejemplo
        testimonios_ejemplo = [
            ('Juan Pérez', 'Constructora ABC', 'Excelente calidad de moldes, muy recomendables.', 'img/clients/client-1.png', 1, 1),
            ('María García', 'Arquitectura XYZ', 'Los moldes de Molpi superaron nuestras expectativas.', 'img/clients/client-2.png', 2, 1),
        ]
        
        for testimonio in testimonios_ejemplo:
            c.execute("""
                INSERT OR IGNORE INTO testimonios 
                (nombre, empresa, testimonio, imagen, orden, activo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, testimonio)
        
        # Insertar promociones de ejemplo
        promociones_ejemplo = [
            ('Oferta Especial Moldes 40x40', 'img/promociones/oferta_40x40.jpg', 'pdf/promociones/catalogo_40x40.pdf', 1, 1),
            ('Descuento Revestimientos', 'img/promociones/descuento_revestimientos.jpg', '', 2, 1),
        ]
        
        for promocion in promociones_ejemplo:
            c.execute("""
                INSERT OR IGNORE INTO promociones 
                (titulo, imagen, cartilla_pdf, orden, activo)
                VALUES (?, ?, ?, ?, ?)
            """, promocion)
        
        conn.commit()
        conn.close()
        
        print("✅ Datos de ejemplo insertados")
        return True
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        return False

def probar_endpoints_locales():
    """Probar que los endpoints funcionan localmente"""
    print("\n🧪 PROBANDO ENDPOINTS LOCALES...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Probar endpoints básicos
            endpoints = [
                '/health',
                '/categorias', 
                '/productos',
                '/productos?incluir_inactivos=true',
                '/subcategorias',
                '/promociones',
                '/testimonios'
            ]
            
            resultados = []
            for endpoint in endpoints:
                try:
                    response = client.get(endpoint)
                    status = response.status_code
                    
                    if status == 200:
                        data = response.get_json()
                        if isinstance(data, list):
                            preview = f"{len(data)} elementos"
                        elif isinstance(data, dict):
                            preview = "objeto JSON"
                        else:
                            preview = "datos"
                    else:
                        preview = "error"
                    
                    resultado = f"  {endpoint}: {status} {'✅' if status == 200 else '❌'} {preview if status == 200 else ''}"
                    print(resultado)
                    resultados.append((endpoint, status == 200))
                    
                except Exception as e:
                    print(f"  {endpoint}: ERROR - {e}")
                    resultados.append((endpoint, False))
            
            exitosos = sum(1 for _, ok in resultados if ok)
            total = len(resultados)
            
            print(f"\n📊 Resultados: {exitosos}/{total} endpoints funcionando")
            return exitosos == total
            
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def generar_reporte():
    """Generar reporte de estado para subir a PythonAnywhere"""
    print("\n📋 GENERANDO REPORTE PARA PYTHONANYWHERE...")
    
    db_path = os.path.join('Python', 'molpi.db')
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        reporte = {
            'fecha_generacion': datetime.now().isoformat(),
            'db_path': db_path,
            'db_size_bytes': os.path.getsize(db_path),
            'tablas': {},
            'endpoints_ok': False
        }
        
        # Información de tablas
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = [row[0] for row in c.fetchall()]
        
        for tabla in tablas:
            c.execute(f"PRAGMA table_info({tabla})")
            columnas = [{'name': row[1], 'type': row[2]} for row in c.fetchall()]
            
            c.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = c.fetchone()[0]
            
            reporte['tablas'][tabla] = {
                'columnas': columnas,
                'registros': count
            }
        
        conn.close()
        
        # Guardar reporte
        with open('reporte_db.json', 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        print("✅ Reporte guardado en reporte_db.json")
        
        # Mostrar resumen
        print(f"\n📊 RESUMEN:")
        print(f"  - Tamaño DB: {reporte['db_size_bytes'] / 1024:.1f} KB")
        print(f"  - Tablas: {len(tablas)}")
        for tabla, info in reporte['tablas'].items():
            print(f"    • {tabla}: {info['registros']} registros, {len(info['columnas'])} columnas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 VERIFICADOR Y MIGRADOR DE BASE DE DATOS MOLPI")
    print("=" * 60)
    
    # Verificar DB actual
    db_ok = verificar_db_local()
    
    if not db_ok:
        print("\n⚠️  Base de datos local no válida. Creando nueva...")
        if not crear_db_completa():
            print("❌ No se pudo crear la base de datos")
            return False
    
    # Insertar datos de ejemplo si la tabla productos está vacía
    db_path = os.path.join('Python', 'molpi.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        c.execute("SELECT COUNT(*) FROM productos")
        productos_count = c.fetchone()[0]
        
        if productos_count == 0:
            print("\n📦 Tabla productos vacía, insertando datos de ejemplo...")
            insertar_datos_ejemplo()
    except:
        print("⚠️  No se pudo verificar productos, saltando inserción de ejemplos")
    finally:
        conn.close()
    
    # Probar endpoints
    endpoints_ok = probar_endpoints_locales()
    
    # Generar reporte
    reporte_ok = generar_reporte()
    
    print("\n" + "=" * 60)
    if db_ok and endpoints_ok and reporte_ok:
        print("🎉 TODO EXITOSO!")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Subir Python/molpi.db a PythonAnywhere")
        print("2. Subir Python/app.py actualizado")
        print("3. Hacer 'Reload' de la aplicación web")
        print("4. Probar https://sgit.pythonanywhere.com/api/health")
        print("\n💡 ARCHIVOS GENERADOS:")
        print("- reporte_db.json (información detallada)")
        print("- Python/molpi.db (base de datos completa)")
    else:
        print("❌ HUBO PROBLEMAS. Revisar errores arriba.")
    
    return db_ok and endpoints_ok and reporte_ok

if __name__ == "__main__":
    main()
