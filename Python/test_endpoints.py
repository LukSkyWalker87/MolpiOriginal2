# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)
# Usar la ruta completa a la base de datos
DB_PATH = 'c:/Users/lucas/OneDrive/Documentos/GitHub/MolpiOriginal2/Python/molpi.db'

@app.route('/productos/linea/20x20', methods=['GET'])
def get_productos_linea_20x20():
    """Obtener productos específicos de la línea 20x20"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
        SELECT id, nombre, descripcion, pdf_url, imagen_url, categoria, subcategoria, 
               precio, activo, fecha_creacion, fecha_modificacion
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
            'categoria': row[5],
            'subcategoria': row[6],
            'precio': row[7],
            'activo': row[8],
            'fecha_creacion': row[9],
            'fecha_modificacion': row[10]
        })
    
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
