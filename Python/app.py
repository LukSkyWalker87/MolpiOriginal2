from flask import Flask, render_template_string, request, jsonify, send_from_directory, send_file, redirect, render_template, url_for, make_response, make_response
from flask_cors import CORS
import os
import sqlite3
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ========= Configuración de Flask =========
# ✅ Instancia única con configuración
app = Flask(__name__, static_folder='../www.molpi.com.ar', static_url_path='')
app.config['SECRET_KEY'] = '123456'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///molpi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

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
    conn = sqlite3.connect('molpi.db')
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
            precio REAL,
            activo INTEGER DEFAULT 1,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
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

@app.route('/productos', methods=['GET'])
def get_productos():
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    # Consulta simple sin JOINs para evitar duplicados
    query = """
        SELECT id, nombre, descripcion, pdf_url, imagen_url, categoria, subcategoria, 
               precio, activo, fecha_creacion, fecha_modificacion
        FROM productos 
        WHERE activo = 1
    """
    params = []
    
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
            'categoria': row[5],
            'subcategoria': row[6],
            'precio': row[7],
            'activo': row[8],
            'fecha_creacion': row[9],
            'fecha_modificacion': row[10]
        })
    
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def add_producto():
    data = request.get_json()
    
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    c.execute("""
        INSERT INTO productos (nombre, descripcion, categoria, subcategoria, pdf_url, imagen_url, precio)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nombre'),
        data.get('descripcion'),
        data.get('categoria'),
        data.get('subcategoria'),
        data.get('pdf_url'),
        data.get('imagen_url'),
        data.get('precio', 0)
    ))
    
    producto_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto agregado correctamente', 'id': producto_id}), 201

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    data = request.get_json()
    
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    c.execute("""
        UPDATE productos 
        SET nombre = ?, descripcion = ?, categoria = ?, subcategoria = ?, 
            pdf_url = ?, imagen_url = ?, precio = ?, fecha_modificacion = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        data.get('nombre'),
        data.get('descripcion'),
        data.get('categoria'),
        data.get('subcategoria'),
        data.get('pdf_url'),
        data.get('imagen_url'),
        data.get('precio', 0),
        producto_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto actualizado correctamente'})

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    # Eliminación lógica
    c.execute("UPDATE productos SET activo = 0 WHERE id = ?", (producto_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Producto eliminado correctamente'})

@app.route('/categorias', methods=['GET'])
def get_categorias():
    conn = sqlite3.connect('molpi.db')
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

@app.route('/subcategorias', methods=['GET'])
def get_subcategorias():
    categoria_id = request.args.get('categoria_id')
    
    conn = sqlite3.connect('molpi.db')
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
#GET /testimonios
@app.route('/testimonios', methods=['GET'])
def obtener_testimonios():
    testimonios = Testimonio.query.order_by(Testimonio.fecha.desc()).all()
    return jsonify([
        {'id': t.id, 'autor': t.autor, 'texto': t.texto, 'fecha': t.fecha.strftime('%Y-%m-%d')}
        for t in testimonios
    ])
#POST /testimonios
@app.route('/testimonios', methods=['POST'])
def crear_testimonio():
    data = request.get_json()
    nuevo = Testimonio(
        autor=data.get('autor'),
        texto=data.get('texto')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'message': 'Testimonio creado correctamente'}), 201

#DELETE /testimonios/<id>
@app.route('/testimonios/<int:id>', methods=['DELETE'])
def borrar_testimonio(id):
    testimonio = Testimonio.query.get_or_404(id)
    db.session.delete(testimonio)
    db.session.commit()
    return jsonify({'message': 'Testimonio eliminado'})



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
