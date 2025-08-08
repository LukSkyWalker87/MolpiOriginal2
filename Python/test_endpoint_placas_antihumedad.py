#!/usr/bin/env python3
"""
Test del endpoint de placas antihumedad
"""

import requests
import json

def test_endpoint_placas_antihumedad():
    """Test del endpoint /productos/placas-antihumedad"""
    
    base_url = "http://127.0.0.1:5000"
    endpoint = "/productos/placas-antihumedad"
    
    print("🧪 Testing endpoint de placas antihumedad...")
    print(f"URL: {base_url}{endpoint}")
    print("-" * 50)
    
    try:
        response = requests.get(f"{base_url}{endpoint}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint responde correctamente")
            print(f"📊 Subcategorías encontradas: {len(data)}")
            
            total_productos = 0
            for subcategoria, productos in data.items():
                print(f"\n📂 {subcategoria}: {len(productos)} productos")
                total_productos += len(productos)
                
                # Mostrar primer producto de cada subcategoría
                if productos:
                    producto = productos[0]
                    print(f"   - {producto['nombre']}")
                    if 'precio' in producto:
                        print(f"   - Precio: ${producto['precio']}")
                    if 'imagen_url' in producto:
                        print(f"   - Imagen: {producto['imagen_url']}")
            
            print(f"\n📈 Total de productos: {total_productos}")
            
            # Verificar estructura esperada
            print("\n🔍 Verificando estructura...")
            for subcategoria, productos in data.items():
                for producto in productos:
                    if 'nombre' not in producto:
                        print(f"❌ Producto sin nombre en {subcategoria}")
                    if 'categoria' not in producto:
                        print(f"❌ Producto sin categoría en {subcategoria}")
                    if 'activo' not in producto:
                        print(f"❌ Producto sin campo activo en {subcategoria}")
            
            print("✅ Estructura validada")
            
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor")
        print("Asegúrate de que el servidor Flask esté ejecutándose en puerto 5000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_endpoint_placas_antihumedad()
