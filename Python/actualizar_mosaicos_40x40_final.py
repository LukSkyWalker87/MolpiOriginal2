import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Mapeo exacto de nombres de productos con sus imágenes de mosaico
mosaicos_40x40 = {
    'Liso 40x40': 'img/products/liso_40_mosaico.png',
    'Riojana': 'img/products/riojana_mosaico.png',
    'Octogonal': 'img/products/octogonal_mosaico.png',
    'Abanico Liso': 'img/products/abanico_liso_mosaico.png',
    'Abanico Rústico': 'img/products/abanico_rustico_mosaico.png',
    'Adoquín Curvo Chico': 'img/products/adoquin_curvo_chico_mosaico.png',
    'Adoquín Curvo Grande': 'img/products/adoquin_curvo_grande_mosaico.png',
    'Adoquín Recto Chico': 'img/products/adoquin_recto_chico_mosaico.png',
    'Adoquín Recto Grande': 'img/products/adoquin_recto_grande_mosaico.png',
    'Laja Española': 'img/products/laja_espaniola_mosaico.png',
    'Laja Ladrillo': 'img/products/laja_ladrillo_mosaico.png',
    'Laja San Luis N°1': 'img/products/laja_san_luis_mosaico.png',
    'Laja San Luis N°2': 'img/products/laja_san_luis_2_mosaico.png',
    'Laja San Luis N°3': 'img/products/laja_san_luis_3_mosaico.png',
    'Laja Cachada': 'img/products/cachada_mosaico.png',
    'Laja N°2 Octogonal': 'img/products/laja_numero_2_octogonal_mosaico.png',
    'Riojana con Bisel': 'img/products/riojana_con_bisel_mosaico.png',
    'Travertino Viejo': 'img/products/travertino_viejo_mosaico.png',
    'Lisa con Bisel': 'img/products/lisa_con_bisel_mosaico.png',
    '64 Panes': 'img/products/64_panes_mosaico.png',
    'Curvo Chico Liso': 'img/products/curvo_chico_liso_mosaico.png',
    'Guarda': 'img/products/guarda_mosaico.png',
    'Zócalo Lineal': 'img/products/zocalo_lineal_mosaico.png',
    'Zócalo Incaico': 'img/products/zocalo_incaico_mosaico.png',
    'Gregoriana': 'img/products/gregoriana_mosaico.png'
}

print("=== ACTUALIZANDO MOSAICOS 40x40 ===")

# Actualizar productos con mosaicos
actualizados = 0
for nombre_exacto, imagen_mosaico in mosaicos_40x40.items():
    c.execute('''
        UPDATE productos 
        SET imagen_mosaico_url = ? 
        WHERE nombre = ? AND subcategoria = "Línea 40x40"
    ''', (imagen_mosaico, nombre_exacto))
    
    if c.rowcount > 0:
        print(f'✓ Actualizado: {nombre_exacto} -> {imagen_mosaico}')
        actualizados += 1
    else:
        print(f'⚠ No encontrado: {nombre_exacto}')

# Confirmar cambios
conn.commit()

print(f"\n✅ Total productos actualizados: {actualizados}")

# Verificar resultado final
c.execute('SELECT COUNT(*) FROM productos WHERE subcategoria = "Línea 40x40" AND imagen_mosaico_url IS NOT NULL AND imagen_mosaico_url != ""')
count = c.fetchone()[0]
print(f'✅ Total productos 40x40 con mosaico: {count}')

# Mostrar productos actualizados
print("\n=== PRODUCTOS 40x40 CON MOSAICO ===")
c.execute('SELECT nombre, imagen_mosaico_url FROM productos WHERE subcategoria = "Línea 40x40" AND imagen_mosaico_url IS NOT NULL AND imagen_mosaico_url != "" ORDER BY nombre')
productos_con_mosaico = c.fetchall()
for prod in productos_con_mosaico:
    print(f'{prod[0]} -> {prod[1]}')

conn.close()
