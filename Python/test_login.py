import requests
import json

# URL de la aplicación Flask
base_url = "http://127.0.0.1:5000"

def test_login_json():
    """Prueba login con petición JSON"""
    login_data = {
        "username": "admin",
        "password": "1234"
    }
    
    response = requests.post(f"{base_url}/login", json=login_data)
    print(f"Login JSON - Status: {response.status_code}")
    print(f"Login JSON - Response: {response.json()}")
    
    return response.status_code == 200

def test_login_form():
    """Prueba login con formulario HTML"""
    login_data = {
        "username": "admin",
        "password": "1234"
    }
    
    response = requests.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"Login Form - Status: {response.status_code}")
    print(f"Login Form - Headers: {response.headers}")
    
    return response.status_code == 302  # Redirección a /admin

if __name__ == "__main__":
    print("=== Pruebas de Login ===")
    
    print("\n1. Probando login con JSON:")
    success_json = test_login_json()
    
    print("\n2. Probando login con formulario:")
    success_form = test_login_form()
    
    print(f"\n=== Resultados ===")
    print(f"Login JSON exitoso: {success_json}")
    print(f"Login Form exitoso: {success_form}")
    
    if success_json and success_form:
        print("\n✅ ¡Ambos tipos de login funcionan correctamente!")
        print("Credenciales: admin/1234")
    else:
        print("\n❌ Hay problemas con el login")
