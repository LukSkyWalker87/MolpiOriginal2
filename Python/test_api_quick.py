import requests

try:
    response = requests.get('http://127.0.0.1:5000/productos')
    print(f"API Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Productos encontrados: {len(data)}")
        if len(data) > 0:
            print(f"Primer producto: {data[0]['nombre']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Error conectando: {e}")
