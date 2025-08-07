#!/usr/bin/env python3
import requests
import json

def reactivar_producto(producto_id):
    url = f"http://127.0.0.1:5000/productos/{producto_id}"
    headers = {'Content-Type': 'application/json'}
    
    producto_data = {
        'nombre': 'Señal Discapacitados',
        'categoria': 'Podotáctiles',
        'subcategoria': 'Discapacidad',
        'descripcion': 'Este se coloca en lugares reservados para accesibilidad. Está pensado para la comunicación hacia las personas videntes. Para dar prioridad o tener precaución para con personas con discapacidad visual.',
        'imagen_url': 'img/products/discapacitado_molde.jpg',
        'imagen_mosaico_url': 'img/products/discapacitado_mosaico.png',
        'precio': 0,
        'precio_usd': 0,
        'pdf_url': '',
        'activo': 1
    }
    
    response = requests.put(url, headers=headers, json=producto_data)
    
    if response.status_code == 200:
        print(f"✅ Producto ID {producto_id} reactivado exitosamente")
        return True
    else:
        print(f"❌ Error reactivando producto ID {producto_id}: {response.status_code} - {response.text}")
        return False

print("🔄 Reactivando producto 'Señal Discapacitados'...")
reactivar_producto(108)
