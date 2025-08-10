#!/usr/bin/env python3
"""
Archivo de debugging específico para PythonAnywhere
Subir como debug_endpoints.py y agregar al app.py
"""

from flask import Flask, jsonify
import sqlite3
import traceback
import os

def crear_endpoints_debug(app):
    """Agregar endpoints de debugging al app Flask"""
    
    @app.route('/api/debug/db-info')
    def debug_db_info():
        """Información detallada de la base de datos"""
        try:
            db_path = 'molpi.db'
            
            if not os.path.exists(db_path):
                return jsonify({
                    'error': 'Base de datos no encontrada',
                    'path': db_path,
                    'exists': False
                }), 500
            
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            # Información básica
            info = {
                'db_path': db_path,
                'db_size': os.path.getsize(db_path),
                'exists': True,
                'tablas': {},
                'errores': []
            }
            
            # Listar tablas
            c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tablas = [row[0] for row in c.fetchall()]
            info['tabla_names'] = tablas
            
            # Información detallada de cada tabla
            for tabla in tablas:
                try:
                    # Estructura
                    c.execute(f"PRAGMA table_info({tabla})")
                    columnas = [{'name': row[1], 'type': row[2], 'notnull': row[3], 'pk': row[5]} for row in c.fetchall()]
                    
                    # Contar registros
                    c.execute(f"SELECT COUNT(*) FROM {tabla}")
                    count = c.fetchone()[0]
                    
                    info['tablas'][tabla] = {
                        'columnas': columnas,
                        'registros': count
                    }
                    
                except Exception as e:
                    info['errores'].append(f"Error en tabla {tabla}: {str(e)}")
            
            conn.close()
            return jsonify(info)
            
        except Exception as e:
            return jsonify({
                'error': f'Error general: {str(e)}',
                'traceback': traceback.format_exc()
            }), 500
    
    @app.route('/api/debug/test-queries')
    def debug_test_queries():
        """Probar las consultas específicas que fallan"""
        try:
            conn = sqlite3.connect('molpi.db')
            c = conn.cursor()
            
            resultados = {}
            
            # Test query categorías
            try:
                c.execute("SELECT id, nombre, descripcion, activo FROM categorias WHERE activo = 1")
                categorias = c.fetchall()
                resultados['categorias'] = {
                    'status': 'OK',
                    'count': len(categorias),
                    'sample': categorias[:3] if categorias else []
                }
            except Exception as e:
                resultados['categorias'] = {
                    'status': 'ERROR',
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                
                # Try simpler query
                try:
                    c.execute("SELECT * FROM categorias LIMIT 3")
                    simple = c.fetchall()
                    resultados['categorias']['simple_query'] = {
                        'status': 'OK',
                        'data': simple
                    }
                except Exception as e2:
                    resultados['categorias']['simple_query'] = {
                        'status': 'ERROR',
                        'error': str(e2)
                    }
            
            # Test query productos
            try:
                c.execute("SELECT id, nombre, categoria, precio FROM productos WHERE activo = 1 LIMIT 5")
                productos = c.fetchall()
                resultados['productos'] = {
                    'status': 'OK',
                    'count': len(productos),
                    'sample': productos
                }
            except Exception as e:
                resultados['productos'] = {
                    'status': 'ERROR',
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
                
                # Try even simpler
                try:
                    c.execute("SELECT COUNT(*) FROM productos")
                    count = c.fetchone()[0]
                    resultados['productos']['count_query'] = {
                        'status': 'OK',
                        'total': count
                    }
                except Exception as e2:
                    resultados['productos']['count_query'] = {
                        'status': 'ERROR',
                        'error': str(e2)
                    }
            
            conn.close()
            return jsonify(resultados)
            
        except Exception as e:
            return jsonify({
                'error': f'Error conectando a DB: {str(e)}',
                'traceback': traceback.format_exc()
            }), 500
    
    @app.route('/api/debug/raw-categorias')
    def debug_raw_categorias():
        """Query más simple para categorías"""
        try:
            conn = sqlite3.connect('molpi.db')
            c = conn.cursor()
            
            # Query más simple posible
            c.execute("SELECT * FROM categorias LIMIT 10")
            rows = c.fetchall()
            
            # Get column names
            c.execute("PRAGMA table_info(categorias)")
            columns = [row[1] for row in c.fetchall()]
            
            conn.close()
            
            return jsonify({
                'columns': columns,
                'data': rows,
                'count': len(rows)
            })
            
        except Exception as e:
            return jsonify({
                'error': str(e),
                'traceback': traceback.format_exc()
            }), 500

# Ejemplo de cómo usar en app.py:
# from debug_endpoints import crear_endpoints_debug
# crear_endpoints_debug(app)
