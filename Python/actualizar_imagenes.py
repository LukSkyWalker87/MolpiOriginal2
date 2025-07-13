import sqlite3
import os

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Mapeo de productos con sus imágenes reales
productos_imagenes = {
    'Ladrillo Colonial': 'img/products/laja_colonial_molde.jpg',
    'Piedra Laja': 'img/products/laja_20_molde.jpg',
    'Vainilla de 3': 'img/products/vainilla_de_3_molde.jpg',
    'Vainilla de 4': 'img/products/vainilla_de_4_molde.jpg',
    'Vainilla de 5': 'img/products/vainilla_de_5_molde.jpg',
    'Vainilla de 6': 'img/products/vainilla_de_6_molde.jpg',
    'Adoquín Rústico': 'img/products/adoquin_individual_molde.jpg',
    'Piedra París': 'img/products/simil_piedra_molde.jpg',
    'Lisa 20x20': 'img/products/lisa_20_molde.jpg',
    'Lisa con Bisel': 'img/products/lisa_con_bisel_molde.jpg',
    'Liso 40x40': 'img/products/liso_40_molde.jpg',
    'Liso 50x50': 'img/products/liso_50_molde.jpg',
    'Octogonal': 'img/products/octogonal_molde.jpg',
    'Riojana': 'img/products/riojana_molde.jpg',
    'Riojana con Bisel': 'img/products/riojana_con_bisel_molde.jpg',
    'Gregoriana': 'img/products/gregoriana_molde.jpg',
    'Corteza': 'img/products/corteza_molde.jpg',
    'Quebracho': 'img/products/quebracho_molde.jpg',
    'Trapezoide': 'img/products/trapezoide_molde.jpg',
    'Ondas': 'img/products/ondas_molde.jpg',
    'Barras': 'img/products/barras_molde.jpg',
    'Círculos': 'img/products/circulos_ciegos_molde.jpg',
    'Abanico Liso': 'img/products/abanico_liso_molde.jpg',
    'Abanico Rústico': 'img/products/abanico_rustico_molde.jpg',
    'Flor Circular': 'img/products/flor_circular_molde.jpg',
    'Deck Símil Madera': 'img/products/deck_simil_madera_molde.jpg',
    'Laja Española': 'img/products/laja_espaniola_molde.jpg',
    'Laja San Juan': 'img/products/laja_san_juan_molde.jpg',
    'Laja San Luis': 'img/products/laja_san_luis_molde.jpg',
    'Laja San Pedro': 'img/products/laja_san_pedro_molde.jpg',
    'Travertino Viejo': 'img/products/travertino_viejo_molde.jpg',
    'Madera 6 cm': 'img/products/madera_6_cm_molde.jpg',
    'Rombo Green': 'img/products/rombo_green_molde.jpg',
    'Recto Green': 'img/products/recto_green_molde.jpg',
    'Círculos Green': 'img/products/circulos_green_molde.jpg',
    'Intertrabado': 'img/products/intertrabado.jpg',
    'Cachada': 'img/products/cachada_molde.jpg',
    'Guarda': 'img/products/guarda_molde.jpg',
    'Piedra Encastrable': 'img/products/piedra_encastrable_molde.jpg',
    'Curvo Chico Liso': 'img/products/curvo_chico_liso_molde.jpg',
    'Discapacitado': 'img/products/discapacitado_molde.jpg',
}

# Actualizar las imágenes de los productos
for nombre, imagen in productos_imagenes.items():
    c.execute("""
        UPDATE productos 
        SET imagen_url = ? 
        WHERE nombre LIKE ?
    """, (imagen, f'%{nombre}%'))

# Confirmar cambios
conn.commit()

print("¡Imágenes actualizadas correctamente!")

# Verificar algunos productos
c.execute("SELECT id, nombre, imagen_url FROM productos WHERE imagen_url IS NOT NULL LIMIT 10")
productos = c.fetchall()
print("\nProductos con imágenes actualizadas:")
for p in productos:
    print(f"ID: {p[0]}, Nombre: {p[1]}, Imagen: {p[2]}")

conn.close()
