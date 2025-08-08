#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/productos/piscinas':
            try:
                # Conectar a la base de datos
                conn = sqlite3.connect('molpi.db')
                cursor = conn.cursor()
                
                # Consulta de productos de piscinas
                cursor.execute("""
                    SELECT id, nombre, descripcion, pdf_url, imagen_url, imagen_mosaico_url, categoria, subcategoria, 
                           precio, precio_usd, activo, fecha_creacion, fecha_modificacion
                    FROM productos 
                    WHERE activo = 1 AND categoria = 'Piscinas'
                    ORDER BY subcategoria, nombre
                """)
                rows = cursor.fetchall()
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
                
                # Respuesta JSON
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = json.dumps(productos_por_subcategoria, ensure_ascii=False, indent=2)
                self.wfile.write(response_data.encode('utf-8'))
                
                print(f"✅ Enviados {sum(len(productos) for productos in productos_por_subcategoria.values())} productos organizados en {len(productos_por_subcategoria)} subcategorías")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print("🚀 Iniciando servidor de prueba en puerto 8001...")
    print("📋 Endpoint disponible: http://127.0.0.1:8001/productos/piscinas")
    
    server = HTTPServer(('127.0.0.1', 8001), TestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Servidor detenido")
        server.shutdown()
