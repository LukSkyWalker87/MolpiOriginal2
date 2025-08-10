from flask import Flask, render_template_string, request, jsonify, send_from_directory, send_file, redirect, render_template, url_for, make_response, make_response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sqlite3
import json
import time
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ========= Configuración de Flask =========
# ✅ Instancia única con configuración
app = Flask(__name__, static_folder='../www.molpi.com.ar', static_url_path='')
app.config['SECRET_KEY'] = '123456'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///molpi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración para archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_file(filename):
    """Verificar si el archivo es una imagen"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in image_extensions

def is_pdf_file(filename):
    """Verificar si el archivo es un PDF"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'pdf'
CORS(app)

# ========= Ruta de la base de datos =========
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

# ========= Configuración de SQLAlchemy =========
db = SQLAlchemy(app)

class Testimonio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# ========= Inicialización de la base de datos =========
with app.app_context():
    db.create_all()

# ========= Página de prueba de login =========
@app.route('/login-test')
def login_test():
    return send_from_directory('.', 'login_test.html')

@app.route('/login-debug')
def login_debug():
    return send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'login-debug.html')

@app.route('/admin/component/productos')
def admin_component_productos():
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'components'), 'productos.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin/component/testimonios')
def admin_component_testimonios():
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'components'), 'testimonios.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin/component/promociones')
def admin_component_promociones():
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'components'), 'promociones.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ========= Login =========
@app.route('/login', methods=['POST'])
def login():
    # Determinar si es JSON o formulario
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username == 'admin' and password == '1234':
            return jsonify({'token': 'valid-token'}), 200
        else:
            return jsonify({'message': 'Credenciales inválidas'}), 401
    else:
        # Formulario HTML
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == '1234':
            return redirect('/admin')
        else:
            return "Credenciales inválidas", 401

# ========= Página principal y archivos estáticos =========
@app.route('/')
def index():
    path = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'index.html'))
    print(f"[DEBUG] Mostrando index desde: {path}")
    return send_file(path)

@app.route('/<path:filename>')
def serve_static(filename):
    folder = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar'))
    return send_from_directory(folder, filename)

# ========= Sección SLIDER =========
@app.route('/datos_slider')
def datos_slider():
    ruta_json = os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'json', 'slider_content.json')
    if os.path.exists(ruta_json):
        with open(ruta_json, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({ "titulo": "", "descripcion": "", "posicion": "left", "activo": False })

@app.route('/admin/slider', methods=['POST'])
def guardar_slider_json():
    try:
        data = request.get_json()
        json_path = os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'data', 'slider_content.json')

        if not os.path.exists(os.path.dirname(json_path)):
            os.makedirs(os.path.dirname(json_path))

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return jsonify({ 'message': 'Cambios guardados correctamente.' })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

# ========= Base de datos: Productos =========
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Tabla principal de productos
    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            categoria TEXT NOT NULL,
            subcategoria TEXT NOT NULL,
            pdf_url TEXT,
            imagen_url TEXT,
            imagen_mosaico_url TEXT,
            precio REAL,
            precio_usd REAL,
            activo INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Migración defensiva: agregar columnas si faltan en DB existente
    def _ensure_column(table, column, col_type):
        c.execute(f"PRAGMA table_info({table})")
        cols = [row[1] for row in c.fetchall()]
        if column not in cols:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
    
    # Asegurar columnas nuevas en 'productos'
    _ensure_column('productos', 'imagen_mosaico_url', 'TEXT')
    _ensure_column('productos', 'precio_usd', 'REAL')
    _ensure_column('productos', 'fecha_creacion', 'TIMESTAMP')
    _ensure_column('productos', 'fecha_modificacion', 'TIMESTAMP')

    # Asegurar columnas esperadas en 'categorias' y 'subcategorias'
    _ensure_column('categorias', 'descripcion', 'TEXT')
    _ensure_column('categorias', 'activo', 'INTEGER')
    _ensure_column('subcategorias', 'descripcion', 'TEXT')
    _ensure_column('subcategorias', 'activo', 'INTEGER')
    
    # Tabla de testimonios
    c.execute("""
        CREATE TABLE IF NOT EXISTS testimonios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT,
            testimonio TEXT,
            imagen TEXT,
            orden INTEGER DEFAULT 0,
            activo INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Asegurar columnas esperadas en 'testimonios'
    _ensure_column('testimonios', 'empresa', 'TEXT')
    _ensure_column('testimonios', 'imagen', 'TEXT')
    _ensure_column('testimonios', 'orden', 'INTEGER')
    _ensure_column('testimonios', 'activo', 'INTEGER')
    _ensure_column('testimonios', 'fecha_creacion', 'TIMESTAMP')
    _ensure_column('testimonios', 'fecha_modificacion', 'TIMESTAMP')

    # Tabla de promociones
    c.execute("""
        CREATE TABLE IF NOT EXISTS promociones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            imagen TEXT,
            cartilla_pdf TEXT,
            orden INTEGER DEFAULT 0,
            activo INTEGER DEFAULT 1,
            fecha_inicio TIMESTAMP,
            fecha_fin TIMESTAMP,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Asegurar columnas esperadas en 'promociones'
    _ensure_column('promociones', 'titulo', 'TEXT')
    _ensure_column('promociones', 'imagen', 'TEXT')
    _ensure_column('promociones', 'cartilla_pdf', 'TEXT')
    _ensure_column('promociones', 'orden', 'INTEGER')
    _ensure_column('promociones', 'activo', 'INTEGER')
    _ensure_column('promociones', 'fecha_inicio', 'TIMESTAMP')
    _ensure_column('promociones', 'fecha_fin', 'TIMESTAMP')
    _ensure_column('promociones', 'fecha_creacion', 'TIMESTAMP')
    _ensure_column('promociones', 'fecha_modificacion', 'TIMESTAMP')
    
    # Tabla de imágenes adicionales para productos
    c.execute("""
        CREATE TABLE IF NOT EXISTS producto_imagenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            imagen_url TEXT,
            orden INTEGER DEFAULT 0,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
    """)
    
    # Tabla de categorías
    c.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            descripcion TEXT,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Tabla de subcategorías
    c.execute("""
        CREATE TABLE IF NOT EXISTS subcategorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria_id INTEGER,
            descripcion TEXT,
            activo INTEGER DEFAULT 1,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id)
        )
    """)
    
    # Insertar categorías por defecto
    categorias_default = [
        ('Pisos y Zócalos', 'Moldes para baldosas lisas o rústicas para interiores y exteriores'),
        ('Revestimientos', 'Moldes para revestimientos símil piedra o madera'),
        ('Podotáctiles - Discapacidad', 'Moldes para baldosas destinadas a señalización urbana'),
        ('Green', 'Moldes ecológicos y sustentables'),
        ('Piscinas', 'Moldes específicos para áreas de piscinas'),
        ('Placas Antihumedad', 'Moldes para placas contra la humedad'),
        ('Insumos', 'Materiales y herramientas complementarias')
    ]
    
    for categoria, desc in categorias_default:
        c.execute("INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?, ?)", (categoria, desc))
    
    # Insertar subcategorías por defecto
    subcategorias_default = [
        ('Línea 20x20', 1),
        ('Línea 40x40', 1),
        ('Línea 50x50', 1),
        ('Revestimientos Piedra', 2),
        ('Revestimientos Madera', 2),
        ('Señalización', 3),
        ('Guías Táctiles', 3),
        ('Eco-Moldes', 4),
        ('Bordes Piscina', 5),
        ('Placas Estándar', 6),
        ('Desmoldantes', 7),
        ('Pigmentos', 7)
    ]
    
    for subcategoria, cat_id in subcategorias_default:
        c.execute("INSERT OR IGNORE INTO subcategorias (nombre, categoria_id) VALUES (?, ?)", (subcategoria, cat_id))
    
    conn.commit()
    conn.close()

init_db()

@app.route('/health', methods=['GET'])
def health():
    try:
        # Verificar DB mínima
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT 1")
        conn.close()
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

@app.route('/productos', methods=['GET'])
def get_productos():
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    incluir_inactivos = request.args.get('incluir_inactivos', 'false').lower() == 'true'
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Consulta simple sin JOINs para evitar duplicados
    query = """
        SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
               precio, precio_usd, activo, fecha_creacion, fecha_modificacion
        FROM productos 
    """
    params = []
    
    # Si no se especifica incluir_inactivos, filtrar solo activos (comportamiento por defecto)
    if not incluir_inactivos:
        query += "WHERE IFNULL(activo, 1) = 1"
    else:
        query += "WHERE 1=1"  # Incluir todos los productos
    
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
    
    return jsonify(productos)

# Aliases con prefijo /api
@app.route('/api/health', methods=['GET'])
def api_health():
    return health()

@app.route('/api/productos', methods=['GET'])
def api_get_productos():
    return get_productos()

@app.route('/api/diagnostico', methods=['GET'])
def api_diagnostico():
    """Diagnóstico rápido del estado de la base y selects básicos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tablas = [r[0] for r in c.fetchall()]

        def columnas(tabla: str):
            c.execute(f"PRAGMA table_info({tabla})")
            return [
                {
                    'cid': r[0], 'name': r[1], 'type': r[2], 'notnull': r[3], 'default': r[4], 'pk': r[5]
                } for r in c.fetchall()
            ]

        diag = {
            'db_path': DB_PATH,
            'tablas': tablas,
        }
        for t in ['productos', 'categorias', 'subcategorias', 'promociones', 'testimonios']:
            diag[f'{t}_columns'] = columnas(t) if t in tablas else None

        tests = {}
        try:
            c.execute("SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, precio, precio_usd, activo, fecha_creacion, fecha_modificacion FROM productos LIMIT 1")
            _ = c.fetchall()
            tests['productos_select'] = 'ok'
        except Exception as e:
            tests['productos_select'] = f'error: {e}'
        try:
            c.execute("SELECT * FROM categorias LIMIT 1")
            _ = c.fetchall()
            tests['categorias_select'] = 'ok'
        except Exception as e:
            tests['categorias_select'] = f'error: {e}'

        diag['select_tests'] = tests
        conn.close()
        return jsonify(diag)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos', methods=['POST'])
def add_producto():
    data = request.get_json()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
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

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    data = request.get_json()
    print(f"[DEBUG] Actualizando producto {producto_id} con datos:", data)
    print(f"[DEBUG] Campo activo recibido:", data.get('activo', 'NO PRESENTE'))
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        UPDATE productos 
        SET nombre = ?, descripcion = ?, categoria = ?, subcategoria = ?, 
            pdf_url = ?, imagen_url = ?, imagen_mosaico_url = ?, precio = ?, precio_usd = ?, activo = ?, fecha_modificacion = CURRENT_TIMESTAMP
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
    
    print(f"[DEBUG] Producto {producto_id} actualizado. Rows affected: {c.rowcount}")
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto actualizado correctamente'})

# ========= Endpoints específicos para líneas de productos =========

@app.route('/productos/linea/20x20', methods=['GET'])
def get_productos_linea_20x20():
    """Obtener productos específicos de la línea 20x20"""
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

@app.route('/productos/linea/40x40', methods=['GET'])
def get_productos_linea_40x40():
    """Obtener productos específicos de la línea 40x40"""
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

@app.route('/productos/linea/50x50', methods=['GET'])
def get_productos_linea_50x50():
    """Obtener productos específicos de la línea 50x50"""
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

# ========= Endpoint específico para Piscinas =========

@app.route('/productos/piscinas', methods=['GET'])
def get_productos_piscinas():
    """Obtener todos los productos de la categoría Piscinas organizados por subcategoría"""
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
    
    # Organizar productos por subcategoría
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

@app.route('/productos/revestimientos', methods=['GET'])
def get_productos_revestimientos():
    """Obtener todos los productos de la categoría Revestimientos organizados por subcategoría"""
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
    
    # Organizar productos por subcategoría
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

@app.route('/productos/placas-antihumedad', methods=['GET'])
def get_productos_placas_antihumedad():
    """Obtener todos los productos de la categoría Placas Antihumedad organizados por subcategoría"""
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
    
    # Organizar productos por subcategoría
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

@app.route('/productos/insumos', methods=['GET'])
def get_productos_insumos():
    """Obtener todos los productos de la categoría Insumos organizados por subcategoría"""
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
    
    # Organizar productos por subcategoría
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

# ========= Fin de endpoints de líneas =========

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    print(f"[DEBUG DELETE] Iniciando eliminación lógica del producto ID: {producto_id}")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Verificar que el producto existe antes de eliminarlo
    c.execute("SELECT id, nombre, activo FROM productos WHERE id = ?", (producto_id,))
    producto_antes = c.fetchone()
    
    if producto_antes:
        print(f"[DEBUG DELETE] Producto encontrado antes de eliminar: {producto_antes}")
        
        # Eliminación lógica
        c.execute("UPDATE productos SET activo = 0 WHERE id = ?", (producto_id,))
        rows_affected = c.rowcount
        print(f"[DEBUG DELETE] Filas afectadas por UPDATE: {rows_affected}")
        
        # Verificar después de la actualización
        c.execute("SELECT id, nombre, activo FROM productos WHERE id = ?", (producto_id,))
        producto_despues = c.fetchone()
        print(f"[DEBUG DELETE] Producto después de eliminar: {producto_despues}")
        
        conn.commit()
        conn.close()
        
        print(f"[DEBUG DELETE] Eliminación lógica completada exitosamente para producto ID: {producto_id}")
        return jsonify({'message': 'Producto eliminado correctamente'})
    else:
        print(f"[DEBUG DELETE] Producto ID {producto_id} no encontrado")
        conn.close()
        return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/categorias', methods=['GET'])
def get_categorias():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM categorias WHERE IFNULL(activo, 1) = 1 ORDER BY nombre")
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

@app.route('/api/categorias', methods=['GET'])
def api_get_categorias():
    return get_categorias()

@app.route('/subcategorias', methods=['GET'])
def get_subcategorias():
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

@app.route('/api/subcategorias', methods=['GET'])
def api_get_subcategorias():
    return get_subcategorias()


@app.route('/admin/guardar_slide/<int:index>', methods=['POST'])
def guardar_slide(index):
    try:
        path = os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'data', 'slider_content.json')
        with open(path, 'r') as f:
            slides = json.load(f)

        data = request.get_json()
        if 0 <= index < len(slides):
            slides[index].update(data)
            with open(path, 'w') as f:
                json.dump(slides, f, indent=2)
            return jsonify({'message': 'Slide actualizado correctamente'})
        else:
            return jsonify({'error': 'Índice fuera de rango'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    from flask import render_template_string

@app.route('/admin/slider')
def admin_slider():
    try:
        slider_path = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'components', 'slider.html'))
        with open(slider_path, encoding='utf-8') as f:
            html = f.read()
        return render_template_string(html)
    except Exception as e:
        return f"Error al cargar slider.html: {str(e)}", 500


#@app.route('/js/<path:filename>')
#def serve_js(filename):
   # return send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'js'), filename)

# ========= Admin y componentes =========
@app.route('/admin')
def admin():
    path = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'admin.html'))
    print(f"[DEBUG] Mostrando admin desde: {path}")
    return send_file(path)

@app.route('/admin.html')
def admin_panel():
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'admin.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/piscinas-dinamico.html')
def piscinas_dinamico():
    """Servir la página dinámica de piscinas"""
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'piscinas_dinamico.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/revestimientos-dinamico.html')
def revestimientos_dinamico():
    """Servir la página dinámica de revestimientos"""
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'revestimientos_dinamico.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/placas-antihumedad-dinamico.html')
def placas_antihumedad_dinamico():
    """Servir la página dinámica de placas antihumedad"""
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'placas_antihumedad_dinamico.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/insumos-dinamico.html')
def insumos_dinamico():
    """Servir la página dinámica de insumos"""
    response = make_response(send_from_directory(os.path.join(app.root_path, '..', 'www.molpi.com.ar'), 'insumos_dinamico.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin.css')
def admin_css():
    return send_from_directory('.', 'admin.css')

@app.route('/admin/component/<section>')
def cargar_componente(section):
    try:
        components_path = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'components'))
        file_path = os.path.join(components_path, f'{section}.html')

        if not os.path.exists(file_path):
            return f"Componente '{section}' no encontrado.", 404

        return send_file(file_path)
    except Exception as e:
        return f"Error al cargar la sección {section}: {str(e)}", 500
    

# ========= Testimonios =========
@app.route('/testimonios', methods=['GET'])
def get_testimonios():
    """Obtener todos los testimonios activos ordenados por orden"""
    try:
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testimonios', methods=['POST'])
def crear_testimonio():
    """Crear un nuevo testimonio"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not all(key in data for key in ['nombre', 'empresa', 'testimonio']):
            return jsonify({'error': 'Faltan campos requeridos: nombre, empresa, testimonio'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener el próximo orden
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testimonios/<int:testimonio_id>', methods=['PUT'])
def actualizar_testimonio(testimonio_id):
    """Actualizar un testimonio existente"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar que el testimonio existe
        cursor.execute('SELECT id FROM testimonios WHERE id = ?', (testimonio_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Testimonio no encontrado'}), 404
        
        # Actualizar testimonio
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testimonios/<int:testimonio_id>', methods=['DELETE'])
def eliminar_testimonio(testimonio_id):
    """Eliminar un testimonio (marcar como inactivo)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar que el testimonio existe
        cursor.execute('SELECT id FROM testimonios WHERE id = ?', (testimonio_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Testimonio no encontrado'}), 404
        
        # Marcar como inactivo en lugar de eliminar
        cursor.execute('''
            UPDATE testimonios 
            SET activo = 0, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (testimonio_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Testimonio eliminado exitosamente'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testimonios/admin', methods=['GET'])
def get_testimonios_admin():
    """Obtener todos los testimonios para administración (incluye inactivos)"""
    try:
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========= ENDPOINTS PROMOCIONES =========

@app.route('/promociones', methods=['GET'])
def get_promociones():
    """Obtener todas las promociones activas"""
    try:
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/promociones', methods=['GET'])
def api_get_promociones():
    return get_promociones()

@app.route('/promociones', methods=['POST'])
def create_promocion():
    """Crear una nueva promoción"""
    try:
        data = request.get_json(silent=True) or {}
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
        return jsonify({'error': str(e)}), 500

@app.route('/promociones/<int:promocion_id>', methods=['PUT'])
def update_promocion(promocion_id):
    """Actualizar una promoción existente"""
    try:
        data = request.get_json(silent=True) or {}
        titulo = data.get('titulo', '')
        imagen = data.get('imagen', '')
        cartilla_pdf = data.get('cartilla_pdf', '')
        activo = data.get('activo', 1)

        if not imagen:
            return jsonify({'error': 'La imagen es requerida'}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar si la promoción existe
        cursor.execute('SELECT id FROM promociones WHERE id = ?', (promocion_id,))
        if not cursor.fetchone():
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
        return jsonify({'error': str(e)}), 500

@app.route('/promociones/<int:promocion_id>', methods=['DELETE'])
def delete_promocion(promocion_id):
    """Eliminar una promoción (marcar como inactiva)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar si la promoción existe
        cursor.execute('SELECT id FROM promociones WHERE id = ?', (promocion_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Promoción no encontrada'}), 404
        
        # Marcar como inactiva en lugar de eliminar
        cursor.execute('''
            UPDATE promociones 
            SET activo = 0, fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (promocion_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Promoción eliminada exitosamente'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/promociones/admin', methods=['GET'])
def get_promociones_admin():
    """Obtener todas las promociones para administración (incluye inactivas)"""
    try:
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
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/promociones/admin', methods=['GET'])
def api_get_promociones_admin():
    return get_promociones_admin()

@app.route('/upload/promocion', methods=['POST'])
def upload_promocion_file():
    """Subir imagen o PDF de promoción"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No se envió ningún archivo'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        
        if file and file.filename and allowed_file(file.filename):
            # Determinar el tipo de archivo y la carpeta de destino
            filename = secure_filename(file.filename)
            timestamp = int(time.time())
            name, ext = os.path.splitext(filename)
            
            if is_image_file(file.filename):
                # Para imágenes
                upload_folder = os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'img', 'promociones')
                unique_filename = f"promo_{timestamp}_{name}{ext}"
                relative_path = f"img/promociones/{unique_filename}"
                file_type = "imagen"
            elif is_pdf_file(file.filename):
                # Para PDFs
                upload_folder = os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'pdf', 'promociones')
                unique_filename = f"cartilla_{timestamp}_{name}{ext}"
                relative_path = f"pdf/promociones/{unique_filename}"
                file_type = "PDF"
            else:
                return jsonify({'error': 'Tipo de archivo no soportado'}), 400
            
            # Crear directorio si no existe
            os.makedirs(upload_folder, exist_ok=True)
            
            # Guardar archivo
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            return jsonify({
                'message': f'{file_type} subido exitosamente',
                'filename': unique_filename,
                'path': relative_path,
                'type': file_type.lower()
            }), 200
        else:
            return jsonify({'error': 'Tipo de archivo no permitido. Solo se permiten imágenes (PNG, JPG, JPEG, GIF, WEBP) y PDFs'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========= Servir imágenes con headers correctos =========
@app.route('/img/<path:filename>')
def serve_images(filename):
    """Servir imágenes con headers correctos y sin cache"""
    folder = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'img'))
    response = send_from_directory(folder, filename)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ========= Servir PDFs con headers correctos =========
@app.route('/pdf/<path:filename>')
def serve_pdfs(filename):
    """Servir archivos PDF con headers correctos"""
    folder = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'pdf'))
    response = send_from_directory(folder, filename)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# ========= Test Endpoint =========
@app.route('/productos-test', methods=['GET'])
def test_productos():
    return jsonify({"mensaje": "Endpoint de prueba funcionando", "ok": True})

@app.route('/test-simple')
def test_simple():
    return "Hola mundo"

# ========= Main =========
if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
