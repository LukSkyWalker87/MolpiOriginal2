import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
cursor = conn.cursor()

# Corregir la URL de Laja Española
cursor.execute("UPDATE productos SET imagen_url = 'img/products/laja_espaniola_molde.jpg' WHERE id = 79")
conn.commit()

print("URL corregida para Laja Española")

# Verificar el cambio
cursor.execute("SELECT nombre, imagen_url FROM productos WHERE id = 79")
result = cursor.fetchone()
print(f"Verificación - Nombre: {result[0]}, Nueva URL: {result[1]}")

conn.close()
