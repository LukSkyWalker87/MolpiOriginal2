import sqlite3
from datetime import datetime

# Conectar a la base de datos
conn = sqlite3.connect('molpi.db')
c = conn.cursor()

print("📦 Agregando productos para todas las categorías...")

# Productos organizados por categoría
productos_completos = {
    'Green': [
        ('Rombo Green', 'Molde para baldosas con diseño de rombo ecológico', 'img/products/rombo_green_molde.jpg', 'Línea Green', 1850.0),
        ('Recto Green', 'Molde para baldosas rectangulares ecológicas', 'img/products/recto_green_molde.jpg', 'Línea Green', 1800.0),
        ('Círculos Green', 'Molde para baldosas con círculos ecológicos', 'img/products/circulos_green_molde.jpg', 'Línea Green', 1900.0),
    ],
    
    'Piscinas': [
        ('Arco Romano', 'Molde para borde de piscina estilo arco romano', 'img/products/piscina_arco_romano_molde.jpg', 'Bordes y Esquinas', 2200.0),
        ('Borde Ballena 40x50', 'Molde para borde ballena de piscina 40x50cm', 'img/products/piscina_borde_ballena_40x50_molde.jpg', 'Bordes y Esquinas', 2100.0),
        ('Escalón 32x18', 'Molde para escalón de piscina 32x18cm', 'img/products/piscina_escalon_32x18_molde.jpg', 'Escalones', 1950.0),
        ('Rejilla', 'Molde para rejilla de desagüe de piscina', 'img/products/piscina_rejilla_molde.jpg', 'Rejillas', 1800.0),
        ('Travertino 50x50', 'Molde para baldosa travertino piscina 50x50cm', 'img/products/piscina_travertino_50x50_molde.jpg', 'Bordes y Esquinas', 2300.0),
        ('Esquinero 50x50', 'Molde para esquina de piscina 50x50cm', 'img/products/piscina_esquinero_50x50_molde.jpg', 'Bordes y Esquinas', 2250.0),
    ],
    
    'Revestimientos': [
        ('Revestimiento 20x40', 'Molde para revestimiento de pared 20x40cm', 'img/products/revestimiento_20x40_molde.jpg', '20x40', 1750.0),
        ('3D Relieve', 'Molde para revestimiento con relieve 3D', 'img/products/revestimiento_3d_mosaico.png', '3D', 2100.0),
        ('Símil Piedra', 'Molde para revestimiento símil piedra', 'img/products/simil_piedra_molde.jpg', '20x40', 1850.0),
        ('Laja 20x40', 'Molde para revestimiento tipo laja 20x40cm', 'img/products/laja_20x40_yeso_mosaico.html', '20x40', 1800.0),
    ],
    
    'Podotáctiles - Discapacidad': [
        ('Discapacitado Guía', 'Molde para baldosa podotáctil de guía', 'img/products/discapacitado_molde.jpg', 'Guías', 1650.0),
        ('Antideslizante 40x40', 'Molde para baldosa antideslizante 40x40cm', 'img/products/antideslizante_40x40_molde.jpg', 'Alertas', 1750.0),
        ('Deck Antideslizante', 'Molde para deck con superficie antideslizante', 'img/products/deckmadera_antideslizante_molde.jpg', 'Alertas', 1900.0),
    ],
    
    'Placas Antihumedad': [
        ('Placa Estándar', 'Placa antihumedad estándar para construcción', 'img/products/plano_20x20.png', 'Estándar', 850.0),
        ('Placa 40x40', 'Placa antihumedad formato 40x40cm', 'img/products/plano_40x40.png', 'Estándar', 1200.0),
        ('Placa 50x50', 'Placa antihumedad formato 50x50cm', 'img/products/plano_50x50.png', 'Estándar', 1500.0),
    ],
    
    'Pisos y Zócalos': [
        # Línea 40x40
        ('Lisa 40x40', 'Molde para baldosa lisa 40x40cm', 'img/products/liso_40_molde.jpg', 'Línea 40x40', 2100.0),
        ('Riojana 40x40', 'Molde para baldosa riojana 40x40cm', 'img/products/riojana_molde.jpg', 'Línea 40x40', 2200.0),
        ('Octogonal 40x40', 'Molde para baldosa octogonal 40x40cm', 'img/products/octogonal_molde.jpg', 'Línea 40x40', 2150.0),
        
        # Línea 50x50  
        ('Lisa 50x50', 'Molde para baldosa lisa 50x50cm', 'img/products/liso_50_molde.jpg', 'Línea 50x50', 2800.0),
        ('Gregoriana 50x50', 'Molde para baldosa gregoriana 50x50cm', 'img/products/gregoriana_molde.jpg', 'Línea 50x50', 2900.0),
        ('Corteza 50x50', 'Molde para baldosa corteza 50x50cm', 'img/products/corteza_molde.jpg', 'Línea 50x50', 2850.0),
        
        # Moldes especiales
        ('Abanico Liso', 'Molde para baldosa abanico liso', 'img/products/abanico_liso_molde.jpg', 'Línea 20x20', 1950.0),
        ('Abanico Rústico', 'Molde para baldosa abanico rústico', 'img/products/abanico_rustico_molde.jpg', 'Línea 20x20', 2000.0),
        ('Flor Circular', 'Molde para baldosa con diseño flor circular', 'img/products/flor_circular_molde.jpg', 'Línea 20x20', 2100.0),
        ('Deck Símil Madera', 'Molde para deck símil madera', 'img/products/deck_simil_madera_molde.jpg', 'Línea 20x20', 2250.0),
    ]
}

# Insertar productos
total_insertados = 0
for categoria, productos in productos_completos.items():
    print(f"\n📁 Agregando productos de {categoria}...")
    
    for nombre, descripcion, imagen_url, subcategoria, precio in productos:
        # Verificar si el producto ya existe
        c.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        if c.fetchone():
            print(f"   ⚠️  {nombre} ya existe, saltando...")
            continue
            
        # Insertar producto
        c.execute("""
            INSERT INTO productos (nombre, descripcion, pdf_url, imagen_url, categoria, subcategoria, precio, activo, fecha_creacion, fecha_modificacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
        """, (
            nombre, 
            descripcion, 
            f'pdf/{nombre.lower().replace(" ", "_")}.pdf',  # PDF genérico
            imagen_url, 
            categoria, 
            subcategoria, 
            precio,
            datetime.now(),
            datetime.now()
        ))
        total_insertados += 1
        print(f"   ✅ {nombre} agregado")

conn.commit()

# Mostrar resumen final
print(f"\n📊 Resumen final:")
print(f"   📦 {total_insertados} productos nuevos agregados")

c.execute("SELECT categoria, COUNT(*) FROM productos GROUP BY categoria ORDER BY categoria")
resumen = c.fetchall()

print("\n   Productos por categoría:")
total_productos = 0
for categoria, cantidad in resumen:
    print(f"   • {categoria}: {cantidad} productos")
    total_productos += cantidad

print(f"\n   🎯 Total general: {total_productos} productos")

conn.close()
print("\n✅ ¡Catálogo completo creado!")
