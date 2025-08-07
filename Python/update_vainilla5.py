import sqlite3

conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Actualizar Vainilla de 5 con imagen de mosaico
c.execute('UPDATE productos SET imagen_mosaico_url = ? WHERE nombre = ?', 
          ('img/products/vainilla_de_6_mosaico.png', 'Vainilla de 5'))

conn.commit()
print(f"Productos actualizados: {c.rowcount}")

# Verificar el cambio
c.execute('SELECT nombre, imagen_mosaico_url FROM productos WHERE nombre = "Vainilla de 5"')
resultado = c.fetchone()
print(f"Resultado: {resultado}")

conn.close()
