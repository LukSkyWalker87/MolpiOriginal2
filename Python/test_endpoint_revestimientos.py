#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

def test_endpoint_revestimientos():
    """Prueba el endpoint /productos/revestimientos"""
    
    try:
        print("🧪 Iniciando prueba del endpoint /productos/revestimientos")
        
        # URL del endpoint
        url = "http://localhost:5000/productos/revestimientos"
        
        print(f"📡 Realizando petición GET a: {url}")
        
        # Realizar petición
        response = requests.get(url, timeout=10)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Parsear JSON
            data = response.json()
            
            print(f"✅ Respuesta exitosa!")
            print(f"📦 Número de subcategorías: {len(data)}")
            
            # Mostrar información por subcategoría
            total_productos = 0
            for subcategoria, productos in data.items():
                print(f"   🔹 {subcategoria}: {len(productos)} productos")
                total_productos += len(productos)
                
                # Mostrar primeros productos de cada subcategoría
                for i, producto in enumerate(productos[:2]):  # Solo primeros 2
                    print(f"      • {producto['nombre']} - ${producto.get('precio', 'Sin precio')} - {producto.get('descripcion', 'Sin descripción')}")
                
                if len(productos) > 2:
                    print(f"      ... y {len(productos) - 2} productos más")
            
            print(f"📈 Total de productos: {total_productos}")
            
            # Verificar estructura de datos
            print(f"\n🔍 Verificando estructura de datos:")
            if data:
                primer_subcategoria = list(data.keys())[0]
                primer_producto = data[primer_subcategoria][0]
                
                campos_esperados = ['id', 'nombre', 'descripcion', 'imagen_url', 'imagen_mosaico_url', 
                                  'categoria', 'subcategoria', 'precio', 'precio_usd', 'activo']
                
                for campo in campos_esperados:
                    if campo in primer_producto:
                        print(f"   ✅ {campo}: {primer_producto[campo]}")
                    else:
                        print(f"   ❌ {campo}: FALTANTE")
            
            print(f"\n🎯 ¡Endpoint funcionando correctamente!")
            return True
            
        else:
            print(f"❌ Error en la respuesta: {response.status_code}")
            print(f"📄 Contenido: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: El servidor no está ejecutándose en localhost:5000")
        print("💡 Asegúrate de que el servidor Flask esté corriendo")
        return False
        
    except requests.exceptions.Timeout:
        print("❌ Error de timeout: El servidor tardó demasiado en responder")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        print(f"📄 Respuesta recibida: {response.text}")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def main():
    print("🧪 Test del endpoint de revestimientos")
    print("=" * 50)
    
    success = test_endpoint_revestimientos()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Todas las pruebas pasaron exitosamente!")
        sys.exit(0)
    else:
        print("❌ Algunas pruebas fallaron")
        sys.exit(1)

if __name__ == "__main__":
    main()
