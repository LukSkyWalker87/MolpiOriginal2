#!/usr/bin/env python
"""Aplicación Flask simplificada que funciona"""

from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/test')
def test():
    return "¡Hola mundo!"

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        conn = sqlite3.connect('molpi.db')
        c = conn.cursor()
        
        c.execute("SELECT id, nombre, categoria, subcategoria FROM productos WHERE activo = 1 LIMIT 5")
        rows = c.fetchall()
        
        productos = []
        for row in rows:
            productos.append({
                'id': row[0],
                'nombre': row[1],
                'categoria': row[2],
                'subcategoria': row[3]
            })
        
        conn.close()
        return jsonify(productos)
        
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5002)
