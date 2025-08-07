import requests
import json

try:
    response = requests.get('http://127.0.0.1:5000/productos')
    productos = response.json()
    
    # Buscar específicamente Green Rectos
    green_rectos = None
    for producto in productos:
        if producto['nombre'] == 'Green Rectos' and producto['categoria'] == 'Green':
            green_rectos = producto
            break
    
    if green_rectos:
        print("🎯 GREEN RECTOS ENCONTRADO:")
        print(f"   ID: {green_rectos['id']}")
        print(f"   Nombre: {green_rectos['nombre']}")
        print(f"   Categoría: {green_rectos['categoria']}")
        print(f"   Activo: {'✅ Sí' if green_rectos['activo'] == 1 else '❌ No'}")
        print(f"   Descripción: {green_rectos.get('descripcion', 'Sin descripción')}")
        print(f"   Imagen molde: {green_rectos.get('imagen_url', 'Sin imagen')}")
        print(f"   Imagen mosaico: {green_rectos.get('imagen_mosaico_url', 'Sin imagen')}")
        
        # Verificar si las imágenes están disponibles
        if green_rectos.get('imagen_url'):
            try:
                img_response = requests.head(f"http://127.0.0.1:5000/{green_rectos['imagen_url']}")
                img_status = "✅ Disponible" if img_response.status_code == 200 else f"❌ Error {img_response.status_code}"
            except:
                img_status = "❌ No accesible"
            print(f"   Estado imagen molde: {img_status}")
        
        if green_rectos.get('imagen_mosaico_url'):
            try:
                img_response = requests.head(f"http://127.0.0.1:5000/{green_rectos['imagen_mosaico_url']}")
                img_status = "✅ Disponible" if img_response.status_code == 200 else f"❌ Error {img_response.status_code}"
            except:
                img_status = "❌ No accesible"
            print(f"   Estado imagen mosaico: {img_status}")
            
    else:
        print("❌ Green Rectos no encontrado en la API")
        
        # Mostrar todos los productos Green disponibles
        green_products = [p for p in productos if p['categoria'] == 'Green' and p['activo'] == 1]
        print(f"\n📋 Productos Green disponibles ({len(green_products)}):")
        for p in green_products:
            print(f"   - {p['nombre']} (ID: {p['id']})")

except Exception as e:
    print(f"❌ Error al conectar con la API: {e}")
