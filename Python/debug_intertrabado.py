import sqlite3
import requests
import os

# Conectar a la base de datos
db_path = 'molpi.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("🔍 Diagnosticando problema de imágenes Intertrabado...")
    
    # Buscar el producto Intertrabado
    cursor.execute('''
        SELECT id, nombre, imagen_url, imagen_mosaico_url, activo 
        FROM productos 
        WHERE nombre = 'Intertrabado' AND categoria = 'Green'
    ''')
    productos = cursor.fetchall()
    
    if productos:
        for producto in productos:
            print(f"\n📦 Producto encontrado:")
            print(f"   ID: {producto[0]}")
            print(f"   Nombre: {producto[1]}")
            print(f"   Activo: {'✅ Sí' if producto[4] == 1 else '❌ No'}")
            print(f"   Imagen molde: {producto[2]}")
            print(f"   Imagen mosaico: {producto[3]}")
            
            # Verificar si las imágenes están disponibles en el servidor
            base_url = "http://127.0.0.1:5000/"
            
            if producto[2]:  # imagen_url
                try:
                    response = requests.head(base_url + producto[2])
                    status = f"✅ {response.status_code}" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   Estado molde: {status}")
                except Exception as e:
                    print(f"   Estado molde: ❌ Error: {e}")
            
            if producto[3]:  # imagen_mosaico_url
                try:
                    response = requests.head(base_url + producto[3])
                    status = f"✅ {response.status_code}" if response.status_code == 200 else f"❌ {response.status_code}"
                    print(f"   Estado mosaico: {status}")
                except Exception as e:
                    print(f"   Estado mosaico: ❌ Error: {e}")
    else:
        print("❌ No se encontró el producto Intertrabado")
    
    # Verificar todos los productos Green para comparar
    print("\n📋 Todos los productos Green:")
    cursor.execute('''
        SELECT id, nombre, imagen_url, imagen_mosaico_url, activo 
        FROM productos 
        WHERE categoria = 'Green'
        ORDER BY nombre
    ''')
    todos_productos = cursor.fetchall()
    
    for p in todos_productos:
        estado = "✅" if p[4] == 1 else "❌"
        molde = "🖼️" if p[2] else "❌"
        mosaico = "🖼️" if p[3] else "❌"
        print(f"   {estado} {p[1]} (ID:{p[0]}) - Molde:{molde} Mosaico:{mosaico}")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    conn.close()

# Verificar la API directamente
print("\n🌐 Verificando API directamente:")
try:
    response = requests.get('http://127.0.0.1:5000/productos')
    if response.status_code == 200:
        productos = response.json()
        intertrabado = [p for p in productos if p['nombre'] == 'Intertrabado' and p['categoria'] == 'Green']
        
        if intertrabado:
            for p in intertrabado:
                print(f"   🎯 Intertrabado en API:")
                print(f"      ID: {p['id']}")
                print(f"      Activo: {p['activo']}")
                print(f"      Imagen molde: {p.get('imagen_url', 'Sin imagen')}")
                print(f"      Imagen mosaico: {p.get('imagen_mosaico_url', 'Sin imagen')}")
        else:
            print("   ❌ Intertrabado no encontrado en API")
    else:
        print(f"   ❌ Error API: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error conectando API: {e}")
