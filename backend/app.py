# ========= IMPORTS Y CONFIGURACIÓN INICIAL =========
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
import json
from datetime import datetime, timedelta
import jwt

# ========= Configuración de Flask =========
app = Flask(__name__, template_folder="../www.molpi.com.ar", static_folder="../www.molpi.com.ar", static_url_path="")
# ========= RUTAS DE PÁGINAS PRINCIPALES (FRONTEND) =========
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/distribuidores')
def distribuidores():
    return render_template('distribuidores.html')

@app.route('/quienes_somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@app.route('/insumos')
def insumos():
    return render_template('insumos.html')

@app.route('/revestimientos')
def revestimientos():
    return render_template('revestimientos.html')

@app.route('/piscinas')
def piscinas():
    return render_template('piscinas.html')

@app.route('/podotactiles')
def podotactiles():
    return render_template('podotactiles.html')

@app.route('/placas_antihumedad')
def placas_antihumedad():
    return render_template('placas_antihumedad.html')

@app.route('/listones')
def listones():
    return render_template('listones.html')

@app.route('/green')
def green():
    return render_template('green.html')
app.config['SECRET_KEY'] = 'molpi-secret-key-2025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///molpi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ========= Rutas para componentes admin (productos, testimonios, promociones) =========
COMPONENTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar', 'components')

@app.route('/admin/component/productos')
def admin_component_productos():
    resp = send_from_directory(COMPONENTS_DIR, 'productos.html')
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/admin/component/testimonios')
def admin_component_testimonios():
    resp = send_from_directory(COMPONENTS_DIR, 'testimonios.html')
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/admin/component/promociones')
def admin_component_promociones():
    resp = send_from_directory(COMPONENTS_DIR, 'promociones.html')
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

# ========= Upload de imágenes de productos =========
@app.route('/upload/producto', methods=['POST'])
def upload_producto():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    # Guardar archivo
    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, str(file.filename))
    file.save(file_path)
    # Devolver ruta relativa para el frontend
    relative_path = os.path.relpath(file_path, os.path.dirname(__file__))
    return jsonify({'path': relative_path.replace('\\', '/')})

# ========= CORS - Configuración para PythonAnywhere =========
# CORS configurado correctamente
CORS(app, resources={r"/*": {
    "origins": [
        "https://www.molpi.com.ar",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]
}})

# ========= Ruta de la base de datos =========
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta de la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

# Verificar que la base de datos existe
if not os.path.exists(DB_PATH):
    logger.error(f"Base de datos no encontrada en: {DB_PATH}")
    # Crear una base de datos vacía si no existe
    conn = sqlite3.connect(DB_PATH)
    conn.close()
    logger.info(f"Base de datos creada en: {DB_PATH}")

# ========= API ENDPOINTS =========

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    try:
        # Verificar conexión a la base de datos
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        return jsonify({
            'status': 'OK',
            'message': 'Molpi API is running',
            'timestamp': datetime.now().isoformat(),
            'database': 'Connected',
            'db_path': DB_PATH
        })
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return jsonify({
            'status': 'ERROR',
            'message': 'Database connection failed',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# ========= Login (unificado) =========
@app.route('/api/login', methods=['POST'])
@app.route('/login', methods=['POST'])
def login():
    """Autenticación unificada: acepta JSON (fetch) o formulario clásico."""
    # Credenciales (puedes moverlas a variables de entorno luego)
    USER = os.environ.get('MOLPI_ADMIN_USER', 'admin')
    PASS = os.environ.get('MOLPI_ADMIN_PASS', 'dumba3110')
    JWT_SECRET = os.environ.get('MOLPI_JWT_SECRET', app.config['SECRET_KEY'])
    JWT_EXP_MINUTES = int(os.environ.get('MOLPI_JWT_EXP_MINUTES', '120'))

    if request.is_json:
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

    if username == USER and password == PASS:
        now = datetime.utcnow()
        payload = {
            'sub': username,
            'role': 'admin',
            'type': 'access',
            'iat': now,
            'exp': now + timedelta(minutes=JWT_EXP_MINUTES)
        }
        refresh_payload = {
            'sub': username,
            'role': 'admin',
            'type': 'refresh',
            'iat': now,
            'exp': now + timedelta(days=7)
        }
        
        try:
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            refresh_token = jwt.encode(refresh_payload, JWT_SECRET, algorithm='HS256')
            return jsonify({
                'token': token, 
                'refresh_token': refresh_token, 
                'expires_in_minutes': JWT_EXP_MINUTES
            }), 200
        except Exception as e:
            print(f"Error generando JWT: {e}")
            return jsonify({'message': 'Error interno del servidor'}), 500
    return jsonify({'message': 'Credenciales inválidas'}), 401

# ======== Decorador de protección ========
from functools import wraps

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        JWT_SECRET = os.environ.get('MOLPI_JWT_SECRET', app.config['SECRET_KEY'])
        auth_header = request.headers.get('Authorization', '')
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()
        elif 'token' in request.args:
            token = request.args.get('token')
        if not token:
            return jsonify({'error': 'Token requerido'}), 401
        try:
            jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except Exception:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return wrapper

def _decode_token(token):
    JWT_SECRET = os.environ.get('MOLPI_JWT_SECRET', app.config['SECRET_KEY'])
    return jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

@app.route('/api/me', methods=['GET'])
@login_required
def me():
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split(' ',1)[1] if auth_header.startswith('Bearer ') else request.args.get('token','')
    data = _decode_token(token)
    return jsonify({'user': data['sub'], 'role': data.get('role','admin')})

@app.route('/api/token/refresh', methods=['POST'])
def refresh_token():
    """Intercambia un refresh_token válido por un nuevo access token."""
    JWT_SECRET = os.environ.get('MOLPI_JWT_SECRET', app.config['SECRET_KEY'])
    JWT_EXP_MINUTES = int(os.environ.get('MOLPI_JWT_EXP_MINUTES', '120'))
    payload = request.get_json(silent=True) or {}
    provided = payload.get('refresh_token')
    if not provided:
        return jsonify({'error': 'refresh_token requerido'}), 400
    try:
        decoded = jwt.decode(provided, JWT_SECRET, algorithms=['HS256'])
        if decoded.get('type') != 'refresh':
            return jsonify({'error': 'Tipo de token inválido'}), 400
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Refresh token expirado'}), 401
    except Exception:
        return jsonify({'error': 'Refresh token inválido'}), 401
    
    now = datetime.utcnow()
    new_payload = {
        'sub': decoded['sub'],
        'role': decoded.get('role','admin'),
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(minutes=JWT_EXP_MINUTES)
    }
    new_token = jwt.encode(new_payload, JWT_SECRET, algorithm='HS256')
    return jsonify({'token': new_token, 'expires_in_minutes': JWT_EXP_MINUTES})

# ========= Productos =========
@app.route('/api/productos', methods=['GET'])
@app.route('/productos', methods=['GET'])
def get_productos():
    """Obtener productos"""
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    query = """
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
    """
    params = []
    
    if not incluir_inactivos:
        query += "WHERE activo = 1"
    else:
        query += "WHERE 1=1"
    
    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)
    
    if subcategoria:
        query += " AND subcategoria = ?"
        params.append(subcategoria)
    
    query += " ORDER BY fecha_creacion DESC"
    
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    
    productos = []
    for row in rows:
        productos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        })
    
    return jsonify({
        'productos': productos,
        'db_path': os.path.abspath(DB_PATH)
    })

@app.route('/api/productos', methods=['POST'])
@app.route('/productos', methods=['POST'])
@login_required
def add_producto():
    """Agregar producto, evitando duplicados por nombre, categoría y subcategoría"""
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Validar si ya existe un producto igual
    c.execute("""
        SELECT id FROM productos WHERE nombre = ? AND categoria = ? AND subcategoria = ?
    """, (
        data.get('nombre'),
        data.get('categoria'),
        data.get('subcategoria')
    ))
    existe = c.fetchone()
    if existe:
        conn.close()
        return jsonify({'error': 'Ya existe un producto con ese nombre, categoría y subcategoría.'}), 409

    c.execute("""
        INSERT INTO productos (nombre, descripcion, categoria, subcategoria, pdf_url, imagen_url, imagen_mosaico_url, precio, precio_usd)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nombre'),
        data.get('descripcion'),
        data.get('categoria'),
        data.get('subcategoria'),
        data.get('pdf_url'),
        data.get('imagen_url'),
        data.get('imagen_mosaico_url'),
        data.get('precio', 0),
        data.get('precio_usd', 0)
    ))
    producto_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'message': 'Producto agregado correctamente', 'id': producto_id}), 201

@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
@app.route('/productos/<int:producto_id>', methods=['PUT'])
@login_required
def update_producto(producto_id):
    """Actualizar producto"""
    data = request.get_json()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        UPDATE productos 
        SET nombre = ?, descripcion = ?, categoria = ?, subcategoria = ?, 
            pdf_url = ?, imagen_url = ?, imagen_mosaico_url = ?, precio = ?, precio_usd = ?, activo = ?, 
            fecha_modificacion = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        data.get('nombre'),
        data.get('descripcion'),
        data.get('categoria'),
        data.get('subcategoria'),
        data.get('pdf_url'),
        data.get('imagen_url'),
        data.get('imagen_mosaico_url'),
        data.get('precio', 0),
        data.get('precio_usd', 0),
        data.get('activo', 1),
        producto_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto actualizado correctamente'})

@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
@login_required
def delete_producto(producto_id):
    """Eliminar producto (eliminación lógica)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT id FROM productos WHERE id = ?", (producto_id,))
    if not c.fetchone():
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    c.execute("UPDATE productos SET activo = 0 WHERE id = ?", (producto_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto eliminado correctamente'})

# ========= Endpoints específicos por línea =========
@app.route('/api/productos/linea/20x20', methods=['GET'])
@app.route('/productos/linea/20x20', methods=['GET'])
def get_productos_linea_20x20():
    """Productos línea 20x20"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 20x20'
        ORDER BY nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos = []
    for row in rows:
        productos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        })
    
    return jsonify(productos)

@app.route('/api/productos/linea/40x40', methods=['GET'])
@app.route('/productos/linea/40x40', methods=['GET'])
def get_productos_linea_40x40():
    """Productos línea 40x40"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 40x40'
        ORDER BY nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos = []
    for row in rows:
        productos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        })
    
    return jsonify(productos)

@app.route('/api/productos/linea/50x50', methods=['GET'])
@app.route('/productos/linea/50x50', methods=['GET'])
def get_productos_linea_50x50():
    """Productos línea 50x50"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Pisos y Zócalos' AND subcategoria = 'Línea 50x50'
        ORDER BY nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos = []
    for row in rows:
        productos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        })
    
    return jsonify(productos)

@app.route('/api/productos/piscinas', methods=['GET'])
@app.route('/productos/piscinas', methods=['GET'])
def get_productos_piscinas():
    """Productos de piscinas organizados por subcategoría"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Piscinas'
        ORDER BY subcategoria, nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos_por_subcategoria = {}
    for row in rows:
        producto = {
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        }
        
        subcategoria = producto['subcategoria']
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        
        productos_por_subcategoria[subcategoria].append(producto)
    
    return jsonify(productos_por_subcategoria)

@app.route('/api/productos/revestimientos', methods=['GET'])
@app.route('/productos/revestimientos', methods=['GET'])
def get_productos_revestimientos():
    """Productos de revestimientos organizados por subcategoría"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Revestimientos'
        ORDER BY subcategoria, nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos_por_subcategoria = {}
    for row in rows:
        producto = {
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        }
        
        subcategoria = producto['subcategoria']
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        
        productos_por_subcategoria[subcategoria].append(producto)
    
    return jsonify(productos_por_subcategoria)

@app.route('/api/productos/placas-antihumedad', methods=['GET'])
@app.route('/productos/placas-antihumedad', methods=['GET'])
def get_productos_placas_antihumedad():
    """Productos de placas antihumedad organizados por subcategoría"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Placas Antihumedad'
        ORDER BY subcategoria, nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos_por_subcategoria = {}
    for row in rows:
        producto = {
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        }
        
        subcategoria = producto['subcategoria']
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        
        productos_por_subcategoria[subcategoria].append(producto)
    
    return jsonify(productos_por_subcategoria)

@app.route('/api/productos/insumos', methods=['GET'])
@app.route('/productos/insumos', methods=['GET'])
def get_productos_insumos():
    """Productos de insumos organizados por subcategoría"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Insumos'
        ORDER BY subcategoria, nombre
    """)
    rows = c.fetchall()
    conn.close()
    
    productos_por_subcategoria = {}
    for row in rows:
        producto = {
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        }
        
        subcategoria = producto['subcategoria']
        if subcategoria not in productos_por_subcategoria:
            productos_por_subcategoria[subcategoria] = []
        
        productos_por_subcategoria[subcategoria].append(producto)
    
    return jsonify(productos_por_subcategoria)

# Endpoint para productos Listones
@app.route('/api/productos/listones', methods=['GET'])
def get_productos_listones():
    """Productos de Listones"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1 AND categoria = 'Listones'
        ORDER BY nombre
    """)
    rows = c.fetchall()
    conn.close()
    productos = []
    for row in rows:
        productos.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'pdf_url': row[3],
            'imagen_url': row[4],
            'imagen_mosaico_url': row[5],
            'categoria': row[6],
            'subcategoria': row[7],
            'precio': row[8],
            'precio_usd': row[9],
            'activo': row[10],
            'fecha_creacion': row[11],
            'fecha_modificacion': row[12]
        })
    return jsonify(productos)

# ========= Testimonios =========
@app.route('/api/testimonios', methods=['GET'])
@app.route('/testimonios', methods=['GET'])
def get_testimonios():
    """Obtener testimonios activos"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nombre, empresa, testimonio, imagen, orden, activo, fecha_creacion
        FROM testimonios 
        WHERE activo = 1 
        ORDER BY orden ASC, id ASC
    ''')
    
    testimonios = []
    for row in cursor.fetchall():
        testimonios.append({
            'id': row[0],
            'nombre': row[1],
            'empresa': row[2],
            'testimonio': row[3],
            'imagen': row[4],
            'orden': row[5],
            'activo': row[6],
            'fecha_creacion': row[7]
        })
    
    conn.close()
    return jsonify(testimonios)

@app.route('/api/testimonios', methods=['POST'])
@app.route('/testimonios', methods=['POST'])
@login_required
def crear_testimonio():
    """Crear testimonio"""
    data = request.get_json()
    
    if not all(key in data for key in ['nombre', 'empresa', 'testimonio']):
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT MAX(orden) FROM testimonios')
    max_orden = cursor.fetchone()[0] or 0
    nuevo_orden = max_orden + 1
    
    cursor.execute('''
        INSERT INTO testimonios (nombre, empresa, testimonio, imagen, orden, activo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['nombre'],
        data['empresa'],
        data['testimonio'],
        data.get('imagen', 'img/clients/client-1.png'),
        data.get('orden', nuevo_orden),
        data.get('activo', 1)
    ))
    
    testimonio_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'id': testimonio_id, 'message': 'Testimonio creado exitosamente'}), 201

@app.route('/api/testimonios/<int:testimonio_id>', methods=['PUT'])
@app.route('/testimonios/<int:testimonio_id>', methods=['PUT'])
@login_required
def actualizar_testimonio(testimonio_id):
    """Actualizar testimonio"""
    data = request.get_json()
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM testimonios WHERE id = ?', (testimonio_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Testimonio no encontrado'}), 404
    
    cursor.execute('''
        UPDATE testimonios 
        SET nombre = ?, empresa = ?, testimonio = ?, imagen = ?, orden = ?, activo = ?,
            fecha_modificacion = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data.get('nombre'),
        data.get('empresa'),
        data.get('testimonio'),
        data.get('imagen', 'img/clients/client-1.png'),
        data.get('orden'),
        data.get('activo', 1),
        testimonio_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Testimonio actualizado exitosamente'})

@app.route('/api/testimonios/<int:testimonio_id>', methods=['DELETE'])
@app.route('/testimonios/<int:testimonio_id>', methods=['DELETE'])
@login_required
def eliminar_testimonio(testimonio_id):
    """Eliminar testimonio"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM testimonios WHERE id = ?', (testimonio_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Testimonio no encontrado'}), 404
    
    cursor.execute('''
        UPDATE testimonios 
        SET activo = 0, fecha_modificacion = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (testimonio_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Testimonio eliminado exitosamente'})

@app.route('/api/testimonios/admin', methods=['GET'])
@app.route('/testimonios/admin', methods=['GET'])
def get_testimonios_admin():
    """Obtener todos los testimonios para admin"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, nombre, empresa, testimonio, imagen, orden, activo, fecha_creacion, fecha_modificacion
        FROM testimonios 
        ORDER BY orden ASC, id ASC
    ''')
    
    testimonios = []
    for row in cursor.fetchall():
        testimonios.append({
            'id': row[0],
            'nombre': row[1],
            'empresa': row[2],
            'testimonio': row[3],
            'imagen': row[4],
            'orden': row[5],
            'activo': row[6],
            'fecha_creacion': row[7],
            'fecha_modificacion': row[8]
        })
    
    conn.close()
    return jsonify(testimonios)

# ========= Promociones =========
@app.route('/api/promociones', methods=['GET'])
@app.route('/promociones', methods=['GET'])
def get_promociones():
    """Obtener promociones activas"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, titulo, imagen, cartilla_pdf, orden 
        FROM promociones 
        WHERE activo = 1 
        ORDER BY orden ASC, id ASC
    ''')
    
    promociones = []
    for row in cursor.fetchall():
        promociones.append({
            'id': row[0],
            'titulo': row[1],
            'imagen': row[2],
            'cartilla_pdf': row[3],
            'orden': row[4]
        })
    
    conn.close()
    return jsonify(promociones)

@app.route('/api/promociones', methods=['POST'])
@app.route('/promociones', methods=['POST'])
@login_required
def create_promocion():
    """Crear promoción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se enviaron datos JSON válidos'}), 400
            
        titulo = data.get('titulo', '')
        imagen = data.get('imagen', '')
        cartilla_pdf = data.get('cartilla_pdf', '')
        
        if not imagen:
            return jsonify({'error': 'La imagen es requerida'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO promociones (titulo, imagen, cartilla_pdf, orden, activo, fecha_creacion, fecha_modificacion)
            VALUES (?, ?, ?, 0, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        ''', (titulo, imagen, cartilla_pdf))
        
        promocion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'message': 'Promoción creada exitosamente',
            'id': promocion_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creando promoción: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/promociones/<int:promocion_id>', methods=['PUT'])
@app.route('/promociones/<int:promocion_id>', methods=['PUT'])
@login_required
def update_promocion(promocion_id):
    """Actualizar promoción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se enviaron datos JSON válidos'}), 400
            
        titulo = data.get('titulo', '')
        imagen = data.get('imagen', '')
        cartilla_pdf = data.get('cartilla_pdf', '')
        activo = data.get('activo', 1)
        
        if not imagen:
            return jsonify({'error': 'La imagen es requerida'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM promociones WHERE id = ?', (promocion_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Promoción no encontrada'}), 404
        
        cursor.execute('''
            UPDATE promociones 
            SET titulo = ?, imagen = ?, cartilla_pdf = ?, activo = ?, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (titulo, imagen, cartilla_pdf, activo, promocion_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Promoción actualizada exitosamente'})
        
    except Exception as e:
        logger.error(f"Error actualizando promoción: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/promociones/<int:promocion_id>', methods=['DELETE'])
@app.route('/promociones/<int:promocion_id>', methods=['DELETE'])
@login_required
def delete_promocion(promocion_id):
    """Eliminar promoción"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM promociones WHERE id = ?', (promocion_id,))
    if not cursor.fetchone():
        return jsonify({'error': 'Promoción no encontrada'}), 404
    
    cursor.execute('''
        UPDATE promociones 
        SET activo = 0, fecha_modificacion = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (promocion_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Promoción eliminada exitosamente'})

@app.route('/api/promociones/admin', methods=['GET'])
@app.route('/promociones/admin', methods=['GET'])
def get_promociones_admin():
    """Obtener todas las promociones para admin"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, titulo, imagen, cartilla_pdf, orden, activo, fecha_inicio, fecha_fin, fecha_creacion, fecha_modificacion
        FROM promociones 
        ORDER BY orden ASC, id ASC
    ''')
    
    promociones = []
    for row in cursor.fetchall():
        promociones.append({
            'id': row[0],
            'titulo': row[1],
            'imagen': row[2],
            'cartilla_pdf': row[3],
            'orden': row[4],
            'activo': row[5],
            'fecha_inicio': row[6],
            'fecha_fin': row[7],
            'fecha_creacion': row[8],
            'fecha_modificacion': row[9]
        })
    
    conn.close()
    return jsonify(promociones)

@app.route('/upload/promocion', methods=['POST'])
@login_required
def upload_promocion():
    """Subir imágenes o PDFs para promociones"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file or not file.filename:
        return jsonify({'error': 'No selected file'}), 400
    
    filename = file.filename
    
    # Validar tipo de archivo
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.pdf'}
    file_ext = os.path.splitext(filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        return jsonify({'error': f'Tipo de archivo no permitido: {file_ext}'}), 400
    
    # Guardar archivo con timestamp para evitar colisiones
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = secure_filename(filename)
    filename_with_timestamp = f"promo_{timestamp}_{safe_filename}"
    
    # Carpeta de uploads
    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'www.molpi.com.ar', 'img', 'promociones')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, filename_with_timestamp)
    file.save(file_path)
    
    # Devolver ruta relativa desde la raíz del sitio web
    relative_path = f'img/promociones/{filename_with_timestamp}'
    return jsonify({'path': relative_path})

# ========= Categorías y Subcategorías =========
@app.route('/api/categorias', methods=['GET'])
@app.route('/categorias', methods=['GET'])
def get_categorias():
    """Obtener categorías"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM categorias WHERE activo = 1 ORDER BY nombre")
    rows = c.fetchall()
    conn.close()
    
    categorias = []
    for row in rows:
        categorias.append({
            'id': row[0],
            'nombre': row[1],
            'descripcion': row[2],
            'activo': row[3]
        })
    
    return jsonify(categorias)

@app.route('/api/subcategorias', methods=['GET'])
@app.route('/subcategorias', methods=['GET'])
def get_subcategorias():
    """Obtener subcategorías"""
    categoria_id = request.args.get('categoria_id')
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if categoria_id:
        c.execute("SELECT * FROM subcategorias WHERE categoria_id = ? AND activo = 1 ORDER BY nombre", (categoria_id,))
    else:
        c.execute("SELECT * FROM subcategorias WHERE activo = 1 ORDER BY nombre")
    
    rows = c.fetchall()
    conn.close()
    
    subcategorias = []
    for row in rows:
        subcategorias.append({
            'id': row[0],
            'nombre': row[1],
            'categoria_id': row[2],
            'descripcion': row[3],
            'activo': row[4]
        })
    
    return jsonify(subcategorias)

# ========= Error Handlers =========
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# ========= Promover a producción =========
import subprocess

@app.route('/api/promover-a-produccion', methods=['POST'])
@login_required
def promover_a_produccion():
    """Ejecuta el script de promoción de UAT a producción"""
    try:
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'promover-a-prod.sh'))
        if not os.path.exists(script_path):
            return jsonify({'success': False, 'error': f'Script no encontrado: {script_path}'}), 500
        # Ejecutar el script
        result = subprocess.run([script_path], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'success': True, 'output': result.stdout})
        else:
            return jsonify({'success': False, 'error': result.stderr, 'output': result.stdout}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ========= Main =========
if __name__ == '__main__':
    app.run(debug=True)
