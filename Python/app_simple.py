#!/usr/bin/env python3
"""
app_simple.py - Versión simplificada para PythonAnywhere
Subir este archivo como app.py (reemplazar el actual)
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os
import traceback

app = Flask(__name__)
CORS(app)

# Configuración
DB_PATH = 'molpi.db'

def get_db_connection():
    """Obtener conexión a la base de datos"""
    return sqlite3.connect(DB_PATH)

@app.route('/health')
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando correctamente',
        'db_exists': os.path.exists(DB_PATH),
        'db_size': os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    })

@app.route('/api/categorias')
def get_categorias():
    """Obtener categorías con query adaptable"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Intentar query completa primero
        try:
            c.execute("SELECT id, nombre, descripcion, activo FROM categorias WHERE activo = 1")
            rows = c.fetchall()
            categorias = []
            for row in rows:
                categorias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2] if row[2] else '',
                    'activo': row[3]
                })
        except sqlite3.OperationalError:
            # Si falla, usar query más simple
            try:
                c.execute("SELECT id, nombre FROM categorias")
                rows = c.fetchall()
                categorias = []
                for row in rows:
                    categorias.append({
                        'id': row[0],
                        'nombre': row[1],
                        'descripcion': '',
                        'activo': 1
                    })
            except Exception as e:
                conn.close()
                return jsonify({'error': f'Error en query simple: {str(e)}'}), 500
        
        conn.close()
        return jsonify(categorias)
        
    except Exception as e:
        return jsonify({
            'error': f'Error obteniendo categorías: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/productos')
def get_productos():
    """Obtener productos con query adaptable"""
    try:
        incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # Intentar query completa primero
        try:
            if incluir_inactivos:
                c.execute("""
                    SELECT id, nombre, descripcion, categoria, subcategoria, 
                           precio, imagen_url, activo 
                    FROM productos 
                    ORDER BY id DESC
                """)
            else:
                c.execute("""
                    SELECT id, nombre, descripcion, categoria, subcategoria, 
                           precio, imagen_url, activo 
                    FROM productos 
                    WHERE activo = 1 
                    ORDER BY id DESC
                """)
            
            rows = c.fetchall()
            productos = []
            for row in rows:
                productos.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2] if row[2] else '',
                    'categoria': row[3],
                    'subcategoria': row[4] if row[4] else '',
                    'precio': row[5],
                    'imagen_url': row[6] if row[6] else '',
                    'activo': row[7]
                })
                
        except sqlite3.OperationalError:
            # Si falla, usar query más simple
            try:
                if incluir_inactivos:
                    c.execute("SELECT id, nombre, categoria, precio FROM productos ORDER BY id DESC")
                else:
                    c.execute("SELECT id, nombre, categoria, precio FROM productos LIMIT 100")
                
                rows = c.fetchall()
                productos = []
                for row in rows:
                    productos.append({
                        'id': row[0],
                        'nombre': row[1],
                        'descripcion': '',
                        'categoria': row[2] if len(row) > 2 else '',
                        'subcategoria': '',
                        'precio': row[3] if len(row) > 3 else 0,
                        'imagen_url': '',
                        'activo': 1
                    })
            except Exception as e:
                conn.close()
                return jsonify({'error': f'Error en query simple productos: {str(e)}'}), 500
        
        conn.close()
        return jsonify(productos)
        
    except Exception as e:
        return jsonify({
            'error': f'Error obteniendo productos: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/subcategorias')
def get_subcategorias():
    """Obtener subcategorías"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT id, nombre, categoria_id FROM subcategorias WHERE activo = 1")
            rows = c.fetchall()
            subcategorias = []
            for row in rows:
                subcategorias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'categoria_id': row[2]
                })
        except sqlite3.OperationalError:
            # Query más simple
            c.execute("SELECT id, nombre FROM subcategorias LIMIT 100")
            rows = c.fetchall()
            subcategorias = []
            for row in rows:
                subcategorias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'categoria_id': 1
                })
        
        conn.close()
        return jsonify(subcategorias)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/promociones')
def get_promociones():
    """Obtener promociones"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT id, titulo, imagen, orden, activo FROM promociones WHERE activo = 1 ORDER BY orden")
            rows = c.fetchall()
            promociones = []
            for row in rows:
                promociones.append({
                    'id': row[0],
                    'titulo': row[1],
                    'imagen': row[2],
                    'orden': row[3],
                    'activo': row[4]
                })
        except sqlite3.OperationalError:
            # Query más simple
            c.execute("SELECT id, titulo FROM promociones LIMIT 10")
            rows = c.fetchall()
            promociones = []
            for row in rows:
                promociones.append({
                    'id': row[0],
                    'titulo': row[1],
                    'imagen': '',
                    'orden': 1,
                    'activo': 1
                })
        
        conn.close()
        return jsonify(promociones)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/testimonios')
def get_testimonios():
    """Obtener testimonios"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT id, nombre, empresa, testimonio, activo FROM testimonios WHERE activo = 1")
            rows = c.fetchall()
            testimonios = []
            for row in rows:
                testimonios.append({
                    'id': row[0],
                    'nombre': row[1],
                    'empresa': row[2] if row[2] else '',
                    'testimonio': row[3],
                    'activo': row[4]
                })
        except sqlite3.OperationalError:
            # Query más simple
            c.execute("SELECT id, nombre, testimonio FROM testimonios LIMIT 10")
            rows = c.fetchall()
            testimonios = []
            for row in rows:
                testimonios.append({
                    'id': row[0],
                    'nombre': row[1],
                    'empresa': '',
                    'testimonio': row[2] if len(row) > 2 else '',
                    'activo': 1
                })
        
        conn.close()
        return jsonify(testimonios)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug/db-info')
def debug_db_info():
    """Debug: información de la base de datos"""
    try:
        if not os.path.exists(DB_PATH):
            return jsonify({'error': 'DB no existe', 'path': DB_PATH}), 500
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # Información básica
        info = {
            'db_path': DB_PATH,
            'db_size': os.path.getsize(DB_PATH),
            'tablas': {}
        }
        
        # Listar tablas
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in c.fetchall()]
        
        for tabla in tablas:
            c.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = c.fetchone()[0]
            
            c.execute(f"PRAGMA table_info({tabla})")
            columnas = [row[1] for row in c.fetchall()]
            
            info['tablas'][tabla] = {
                'registros': count,
                'columnas': columnas
            }
        
        conn.close()
        return jsonify(info)
        
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True)
