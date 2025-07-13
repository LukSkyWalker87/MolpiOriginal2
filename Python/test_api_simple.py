import requests
import json

print("🔍 Probando API corregida...")
try:
    response = requests.get('http://127.0.0.1:5000/productos')
    
    if response.status_code == 200:
        productos = response.json()
        print(f"✅ API responde con {len(productos)} productos")
        
        # Verificar IDs únicos
        ids = [p['id'] for p in productos]
        ids_unicos = set(ids)
        
        if len(ids) == len(ids_unicos):
            print("✅ Todos los IDs son únicos")
        else:
            print(f"⚠️ Hay {len(ids) - len(ids_unicos)} productos duplicados")
            
        # Verificar producto específico ID 39
        productos_39 = [p for p in productos if p['id'] == 39]
        print(f"🔍 Producto ID 39 aparece {len(productos_39)} vez(es)")
        
        if productos_39:
            print(f"   Nombre: {productos_39[0]['nombre']}")
            
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
