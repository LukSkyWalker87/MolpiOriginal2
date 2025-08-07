import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

# Primero, ver qué productos 40x40 tenemos
print("=== PRODUCTOS 40x40 EXISTENTES ===")
c.execute('SELECT id, nombre, imagen_url FROM productos WHERE linea = "40x40" ORDER BY nombre')
productos_existentes = c.fetchall()

for producto in productos_existentes:
    print(f"ID: {producto[0]} | Nombre: {producto[1]}")

print(f"\nTotal productos 40x40: {len(productos_existentes)}")

# Lista de mosaicos y sus nombres aproximados
mosaicos_40x40 = {
    'Liso': 'img/products/liso_40_mosaico.png',
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
    'Laja San Luis': 'img/products/laja_san_luis_mosaico.png',
    'Cachada': 'img/products/cachada_mosaico.png',
    'Octogonal': 'img/products/laja_numero_2_octogonal_mosaico.png',
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

print("\n=== ACTUALIZANDO MOSAICOS ===")

# Actualizar productos con mosaicos
actualizados = 0
for nombre_buscar, imagen_mosaico in mosaicos_40x40.items():
    c.execute('''
        UPDATE productos 
        SET imagen_mosaico_url = ? 
        WHERE nombre LIKE ? AND linea = "40x40"
    ''', (imagen_mosaico, f'%{nombre_buscar}%'))
    
    if c.rowcount > 0:
        print(f'✓ Actualizado: {nombre_buscar} -> {imagen_mosaico}')
        actualizados += 1
    else:
        print(f'⚠ No encontrado: {nombre_buscar}')

# Confirmar cambios
conn.commit()

print(f"\n✅ Total productos actualizados: {actualizados}")

# Verificar resultado final
c.execute('SELECT COUNT(*) FROM productos WHERE linea = "40x40" AND imagen_mosaico_url IS NOT NULL AND imagen_mosaico_url != ""')
count = c.fetchone()[0]
print(f'✅ Total productos 40x40 con mosaico: {count}')

conn.close()
