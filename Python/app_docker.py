from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuración
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')
PORT = int(os.environ.get('PORT', 8080))

def get_db_connection():
    """Obtener conexión a la base de datos"""
    return sqlite3.connect(DB_PATH)

@app.route('/')
def index():
    """Servir admin.html como página principal (desde www.molpi.com.ar si existe)"""
    www_admin = os.path.join('..', 'www.molpi.com.ar', 'admin.html')
    if os.path.exists(www_admin):
        return send_file(www_admin)
    return send_file('../frontend/admin.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos del frontend (prioriza www.molpi.com.ar si existe)"""
    # Primero intenta servir desde www.molpi.com.ar
    www_path = os.path.join('..', 'www.molpi.com.ar')
    front_path = os.path.join('..', 'frontend')
    if os.path.exists(os.path.join(www_path, filename)):
        return send_from_directory(www_path, filename)
    # Si no existe ahí, servir desde frontend
    return send_from_directory(front_path, filename)

@app.route('/env.js')
def dynamic_env_js():
    """Generar env.js dinámico apuntando a /api para evitar CORS"""
    content = """
// Generado por app_docker
window.env = { API_URL: '/api' };
"""
    return app.response_class(content, mimetype='application/javascript')

@app.route('/health')
@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Molpi API funcionando',
        'timestamp': datetime.now().isoformat(),
        'db_exists': os.path.exists(DB_PATH),
        'db_size': os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    })

@app.route('/api/categorias')
def get_categorias():
    """Obtener categorías"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Query adaptable - intenta columnas completas primero
        try:
            c.execute("SELECT id, nombre, descripcion, activo FROM categorias WHERE activo = 1")
            rows = c.fetchall()
            categorias = []
            for row in rows:
                categorias.append({
                    'id': row[0],
                    'nombre': row[1],
                    'descripcion': row[2] or '',
                    'activo': row[3]
                })
        except sqlite3.OperationalError:
            # Fallback a query más simple
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
        
        conn.close()
        return jsonify(categorias)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/productos')
def get_productos():
    """Obtener productos"""
    try:
        incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
        
        conn = get_db_connection()
        c = conn.cursor()
        
        # Query adaptable
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
                    'descripcion': row[2] or '',
                    'categoria': row[3],
                    'subcategoria': row[4] or '',
                    'precio': row[5],
                    'imagen_url': row[6] or '',
                    'activo': row[7]
                })
                
        except sqlite3.OperationalError:
            # Fallback a query más simple
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
        
        conn.close()
        return jsonify(productos)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/subcategorias')
def get_subcategorias():
    """Obtener subcategorías"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        try:
            c.execute("SELECT id, nombre, categoria_id FROM subcategorias WHERE activo = 1")
        except sqlite3.OperationalError:
            c.execute("SELECT id, nombre FROM subcategorias LIMIT 100")
        
        rows = c.fetchall()
        subcategorias = []
        for row in rows:
            subcategorias.append({
                'id': row[0],
                'nombre': row[1],
                'categoria_id': row[2] if len(row) > 2 else 1
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
        except sqlite3.OperationalError:
            c.execute("SELECT id, titulo FROM promociones LIMIT 10")
        
        rows = c.fetchall()
        promociones = []
        for row in rows:
            promociones.append({
                'id': row[0],
                'titulo': row[1],
                'imagen': row[2] if len(row) > 2 else '',
                'orden': row[3] if len(row) > 3 else 1,
                'activo': row[4] if len(row) > 4 else 1
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
        except sqlite3.OperationalError:
            c.execute("SELECT id, nombre, testimonio FROM testimonios LIMIT 10")
        
        rows = c.fetchall()
        testimonios = []
        for row in rows:
            testimonios.append({
                'id': row[0],
                'nombre': row[1],
                'empresa': row[2] if len(row) > 2 else '',
                'testimonio': row[3] if len(row) > 3 else row[2],
                'activo': row[4] if len(row) > 4 else 1
            })
        
        conn.close()
        return jsonify(testimonios)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"🚀 Iniciando Molpi API en puerto {PORT}")
    print(f"📊 Base de datos: {DB_PATH}")
    print(f"📂 Directorio: {os.getcwd()}")
    
    if os.path.exists(DB_PATH):
        print(f"✅ DB encontrada: {os.path.getsize(DB_PATH):,} bytes")
    else:
        print("❌ DB no encontrada")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
