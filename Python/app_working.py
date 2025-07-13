#!/usr/bin/env python
"""Test simple Flask app"""

from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/productos', methods=['GET'])
def get_productos():
    print("[DEBUG] get_productos called!")
    
    # Verificar si la base de datos existe
    db_path = 'molpi.db'
    if not os.path.exists(db_path):
        print(f"[ERROR] Database {db_path} does not exist!")
        return jsonify([])
    
    print(f"[DEBUG] Database path: {os.path.abspath(db_path)}")
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        query = "SELECT COUNT(*) FROM productos WHERE activo = 1"
        c.execute(query)
        count = c.fetchone()[0]
        print(f"[DEBUG] Found {count} active products")
        
        if count == 0:
            conn.close()
            return jsonify([])
        
        # Obtener algunos productos
        query = "SELECT id, nombre, categoria, subcategoria FROM productos WHERE activo = 1 LIMIT 5"
        c.execute(query)
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
        print(f"[DEBUG] Returning {len(productos)} products")
        return jsonify(productos)
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return jsonify([])

@app.route('/test-debug')
def test_debug():
    print("[DEBUG] test_debug called!")
    return "Test debug endpoint working"

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)
