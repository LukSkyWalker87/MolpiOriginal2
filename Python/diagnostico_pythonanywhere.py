#!/usr/bin/env python3
"""
Script de diagnóstico para PythonAnywhere
Subir este archivo a /home/sgit/mysite/ y ejecutar desde consola
"""

import sqlite3
import os
import sys
import traceback
from datetime import datetime

def diagnosticar_todo():
    """Diagnóstico completo del sistema"""
    print("=" * 60)
    print("🔍 DIAGNÓSTICO COMPLETO - MOLPI PYTHONANYWHERE")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now()}")
    print(f"🐍 Python: {sys.version}")
    print(f"📂 Directorio actual: {os.getcwd()}")
    
    # 1. Verificar archivos
    print("\n1️⃣ VERIFICANDO ARCHIVOS...")
    archivos = ['molpi.db', 'app.py']
    for archivo in archivos:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"✅ {archivo}: {size:,} bytes")
        else:
            print(f"❌ {archivo}: NO EXISTE")
    
    # 2. Verificar base de datos
    print("\n2️⃣ VERIFICANDO BASE DE DATOS...")
    try:
        if not os.path.exists('molpi.db'):
            print("❌ molpi.db no existe")
            return
        
        conn = sqlite3.connect('molpi.db')
        c = conn.cursor()
        
        # Listar tablas
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = [row[0] for row in c.fetchall()]
        print(f"📋 Tablas: {', '.join(tablas)}")
        
        # Verificar datos en cada tabla
        for tabla in ['productos', 'categorias', 'subcategorias', 'promociones', 'testimonios']:
            if tabla in tablas:
                c.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = c.fetchone()[0]
                print(f"  📊 {tabla}: {count} registros")
                
                # Verificar columnas
                c.execute(f"PRAGMA table_info({tabla})")
                columnas = [row[1] for row in c.fetchall()]
                print(f"     📝 Columnas: {', '.join(columnas)}")
            else:
                print(f"  ❌ {tabla}: NO EXISTE")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando DB: {e}")
        traceback.print_exc()
    
    # 3. Probar queries específicas que fallan
    print("\n3️⃣ PROBANDO QUERIES ESPECÍFICAS...")
    try:
        conn = sqlite3.connect('molpi.db')
        c = conn.cursor()
        
        # Query categorías
        try:
            c.execute("SELECT id, nombre, descripcion, activo FROM categorias WHERE activo = 1")
            categorias = c.fetchall()
            print(f"✅ Query categorías: {len(categorias)} activas")
            for cat in categorias[:3]:
                print(f"     • {cat[1]}")
        except Exception as e:
            print(f"❌ Query categorías falló: {e}")
        
        # Query productos
        try:
            c.execute("SELECT id, nombre, categoria, precio FROM productos WHERE activo = 1 LIMIT 5")
            productos = c.fetchall()
            print(f"✅ Query productos: {len(productos)} encontrados")
            for prod in productos:
                print(f"     • {prod[1]} - {prod[2]}")
        except Exception as e:
            print(f"❌ Query productos falló: {e}")
            
            # Intentar query más simple
            try:
                c.execute("SELECT COUNT(*) FROM productos")
                count = c.fetchone()[0]
                print(f"     ℹ️ Total productos en DB: {count}")
            except Exception as e2:
                print(f"     ❌ Ni siquiera COUNT funciona: {e2}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error probando queries: {e}")
    
    # 4. Verificar imports y Flask
    print("\n4️⃣ VERIFICANDO IMPORTS...")
    try:
        import flask
        print(f"✅ Flask: {flask.__version__}")
    except Exception as e:
        print(f"❌ Flask: {e}")
    
    try:
        import flask_cors
        print(f"✅ Flask-CORS: Disponible")
    except Exception as e:
        print(f"❌ Flask-CORS: {e}")
    
    # 5. Probar app.py
    print("\n5️⃣ PROBANDO APP.PY...")
    try:
        # Solo verificar que se puede importar
        sys.path.insert(0, '.')
        
        # Verificar que el archivo existe y es legible
        with open('app.py', 'r') as f:
            content = f.read()
            print(f"✅ app.py leído: {len(content):,} caracteres")
            
            # Buscar configuraciones importantes
            if 'DB_PATH' in content:
                print("✅ DB_PATH encontrado en app.py")
            if 'init_db()' in content:
                print("✅ init_db() encontrado en app.py")
            if '@app.route' in content:
                routes = content.count('@app.route')
                print(f"✅ Rutas encontradas: {routes}")
        
    except Exception as e:
        print(f"❌ Error verificando app.py: {e}")
        traceback.print_exc()
    
    # 6. Probar creación de app Flask
    print("\n6️⃣ PROBANDO CREACIÓN DE APP...")
    try:
        from flask import Flask
        test_app = Flask(__name__)
        
        @test_app.route('/test')
        def test():
            return {'status': 'test ok'}
        
        with test_app.test_client() as client:
            resp = client.get('/test')
            print(f"✅ Test Flask app: {resp.status_code}")
            
    except Exception as e:
        print(f"❌ Error creando test app: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    diagnosticar_todo()
