import requests
import json

try:
    print("🔍 Probando API de productos...")
    response = requests.get('http://127.0.0.1:5000/productos')
    
    if response.status_code == 200:
        productos = response.json()
        print(f"✅ API responde correctamente con {len(productos)} productos")
        
        # Verificar duplicados por ID
        ids = [p['id'] for p in productos]
        ids_unicos = set(ids)
        
        if len(ids) != len(ids_unicos):
            print("⚠️ PROBLEMA: Hay IDs duplicados en la respuesta de la API!")
            
            # Encontrar duplicados
            duplicados = {}
            for producto in productos:
                id_prod = producto['id']
                if id_prod in duplicados:
                    duplicados[id_prod].append(producto['nombre'])
                else:
                    duplicados[id_prod] = [producto['nombre']]
            
            for id_prod, nombres in duplicados.items():
                if len(nombres) > 1:
                    print(f"   ID {id_prod}: {nombres}")
                    
        else:
            print("✅ No hay IDs duplicados en la API")
            
        # Verificar si hay productos con el mismo nombre
        nombres = [p['nombre'] for p in productos]
        nombres_unicos = set(nombres)
        
        if len(nombres) != len(nombres_unicos):
            print("⚠️ Hay nombres duplicados:")
            nombres_contados = {}
            for nombre in nombres:
                nombres_contados[nombre] = nombres_contados.get(nombre, 0) + 1
            
            for nombre, count in nombres_contados.items():
                if count > 1:
                    print(f"   '{nombre}': {count} veces")
        else:
            print("✅ No hay nombres duplicados")
            
        # Mostrar producto ID 39 específicamente
        producto_39 = [p for p in productos if p['id'] == 39]
        if producto_39:
            print(f"\n🔍 Producto ID 39: {producto_39[0]['nombre']}")
            print(f"   Aparece {len(producto_39)} vez(es) en la respuesta de la API")
        
    else:
        print(f"❌ Error en API: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
