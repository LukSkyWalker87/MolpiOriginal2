import requests

print("🔍 Verificando API de productos...")

try:
    response = requests.get('http://127.0.0.1:5000/productos')
    
    if response.status_code == 200:
        data = response.json()
        ids = [p['id'] for p in data]
        
        print(f"📊 Resultados:")
        print(f"   Total productos: {len(data)}")
        print(f"   IDs únicos: {len(set(ids))}")
        
        if len(data) == len(set(ids)):
            print("✅ API funciona correctamente - NO hay duplicados")
            
            # Mostrar algunos ejemplos
            print("\n📦 Primeros 5 productos:")
            for i, p in enumerate(data[:5]):
                print(f"   {i+1}. ID {p['id']}: {p['nombre']} ({p['categoria']})")
                
        else:
            print("⚠️ Aún hay duplicados en la API")
            duplicated_ids = [id_ for id_ in set(ids) if ids.count(id_) > 1]
            print(f"IDs duplicados: {duplicated_ids[:5]}")
            
    else:
        print(f"❌ Error HTTP: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ No se puede conectar al servidor. ¿Está corriendo Flask?")
except Exception as e:
    print(f"❌ Error: {e}")
