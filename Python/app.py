from flask import Flask, render_template_string, request, jsonify, send_from_directory, send_file, redirect, render_template, url_for
from flask_cors import CORS
import os
import sqlite3
import json

# ========= Configuración de Flask =========
# ✅ Instancia única con configuración
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
CORS(app)

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
        
        if username == 'admin' and password == 'admin123':
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
    c.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            pdf_url TEXT,
            imagen_url TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/productos', methods=['GET'])
def get_productos():
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    c.execute("SELECT * FROM productos")
    rows = c.fetchall()
    conn.close()
    return jsonify([{
        'id': row[0],
        'nombre': row[1],
        'descripcion': row[2],
        'pdf_url': row[3],
        'imagen_url': row[4]
    } for row in rows])

@app.route('/productos', methods=['POST'])
def add_producto():
    data = request.get_json()
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    c.execute("INSERT INTO productos (nombre, descripcion, pdf_url, imagen_url) VALUES (?, ?, ?, ?)",
              (data['nombre'], data['descripcion'], data['pdf_url'], data['imagen_url']))
    conn.commit()
    conn.close()
    return jsonify({ 'message': 'Producto agregado' })


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


@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    c.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    conn.commit()
    conn.close()
    return jsonify({ 'message': 'Producto eliminado' })

# ========= Admin y componentes =========
@app.route('/admin')
def admin():
    path = os.path.abspath(os.path.join(app.root_path, '..', 'www.molpi.com.ar', 'admin.html'))
    print(f"[DEBUG] Mostrando admin desde: {path}")
    return send_file(path)

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
    

# ========= Main =========
if __name__ == '__main__':
    app.run(debug=True)
