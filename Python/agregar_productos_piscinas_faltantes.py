#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def agregar_productos_piscinas():
    """
    Agrega los productos de piscinas faltantes basados en piscinas.html
    """
    
    # Productos que deben estar según piscinas.html
    productos_html = [
        {
            'nombre': 'Travertino 50x50x3cm',
            'descripcion': 'Molde para baldosa travertino piscina 50x50cm. Modelo disponible en 3cm y 2,2cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2300.00,
            'precio_usd': 7.67,
            'imagen_url': 'img/products/piscina_travertino_50x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_travertino_50x50_mosaico.png'
        },
        {
            'nombre': 'Borde Recto con Diente',
            'descripcion': 'Un diseño para dar una terminación más delicada a la piscina.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2200.00,
            'precio_usd': 7.33,
            'imagen_url': 'img/products/piscina_travertino_50x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_borde_recto_diente_50x50.png'
        },
        {
            'nombre': 'Borde Recto 40x50',
            'descripcion': 'Molde para borde recto de piscina 40x50cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2100.00,
            'precio_usd': 7.00,
            'imagen_url': 'img/products/piscina_borderecto_40x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_borderecto_40x50_mosaico.png'  # Nota: era .html, cambié a .png
        },
        {
            'nombre': 'Escalón 50x32cm',
            'descripcion': 'Molde para escalón de piscina 32x18cm. Modelo con alzada de 50x18cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Escalones',
            'precio': 1950.00,
            'precio_usd': 6.50,
            'imagen_url': 'img/products/piscina_escalon_32x18_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_escalon_32x18_mosaico.png'  # Nota: era .html, cambié a .png
        },
        {
            'nombre': 'Arco Romano',
            'descripcion': 'Molde para borde piscina estilo arco romano. 2 y 3 metros de diámetro.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2200.00,
            'precio_usd': 7.33,
            'imagen_url': 'img/products/piscina_arco_romano_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_arco_romano_mosaico.png'
        },
        {
            'nombre': 'Borde Ballena 40x50x3cm',
            'descripcion': 'Molde para borde ballena de piscina 40x50cm. Su forma evita el reingreso de agua y otros cuerpos. Modelo disponible en 3cm y 2,2cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2100.00,
            'precio_usd': 7.00,
            'imagen_url': 'img/products/piscina_borde_ballena_40x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_borde_ballena_40x50_mosaico.png'
        },
        {
            'nombre': 'Esquinero 50x50cm',
            'descripcion': 'Molde para esquina de piscina 50x50cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2250.00,
            'precio_usd': 7.50,
            'imagen_url': 'img/products/piscina_esquinero_50x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_esquinero_50x50_mosaico.png'
        },
        {
            'nombre': 'Esquinero Invertido 40x40cm',
            'descripcion': 'Molde para esquinero invertido de piscina 40x40cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2150.00,
            'precio_usd': 7.17,
            'imagen_url': 'img/products/piscina_esquinero_invertido_50x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_esquinero_invertido_50x50_mosaico.png'
        },
        {
            'nombre': 'Rejilla 50x25x4cm',
            'descripcion': 'Molde para rejilla de desagüe de piscina. Para evitar el agua estancada por el desborde. 2 piezas por molde.',
            'categoria': 'Piscinas',
            'subcategoria': 'Rejillas',
            'precio': 1800.00,
            'precio_usd': 6.00,
            'imagen_url': 'img/products/piscina_rejilla_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_rejilla_mosaico.png'
        },
        {
            'nombre': 'Esquina Rejilla 25x25x4cm',
            'descripcion': 'Molde para esquina rejilla de desagüe de piscina 25x25x4cm. 4 piezas por molde para la unión en las esquinas.',
            'categoria': 'Piscinas',
            'subcategoria': 'Rejillas',
            'precio': 1700.00,
            'precio_usd': 5.67,
            'imagen_url': 'img/products/piscina_esquina_rejilla_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_esquina_rejilla_mosaico.png'
        },
        {
            'nombre': 'Deck Antideslizante con Diente',
            'descripcion': 'Molde para deck antideslizante con diente para piscina. Permite obtener un espacio seguro, atérmico y antideslizante.',
            'categoria': 'Piscinas',
            'subcategoria': 'Deck',
            'precio': 2400.00,
            'precio_usd': 8.00,
            'imagen_url': 'img/products/deckmadera_antideslizante_molde.jpg',
            'imagen_mosaico_url': 'img/products/deckmadera_antideslizanteamarillo_mosaico.png'
        },
        {
            'nombre': 'Deck Travertino',
            'descripcion': 'Molde para deck travertino para piscina. Mantiene la misma estética que los bordes de piscina.',
            'categoria': 'Piscinas',
            'subcategoria': 'Deck',
            'precio': 2350.00,
            'precio_usd': 7.83,
            'imagen_url': 'img/products/piscina_deck_travertino_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_deck_travertino_mosaico.png'
        },
        {
            'nombre': 'Travertino Piscina 40x40x2,2cm',
            'descripcion': 'Molde para baldosa travertino piscina 40x40x2,2cm.',
            'categoria': 'Piscinas',
            'subcategoria': 'Bordes y Esquinas',
            'precio': 2000.00,
            'precio_usd': 6.67,
            'imagen_url': 'img/products/piscina_travertino_50x50_molde.jpg',
            'imagen_mosaico_url': 'img/products/piscina_travertino_50x50_mosaico.png'
        }
    ]
    
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('molpi.db')
        cursor = conn.cursor()
        
        print("Verificando productos existentes en la categoría Piscinas...")
        
        # Verificar productos existentes
        cursor.execute('SELECT nombre FROM productos WHERE categoria = ?', ('Piscinas',))
        productos_existentes = [row[0] for row in cursor.fetchall()]
        
        print(f"Productos existentes en Piscinas: {len(productos_existentes)}")
        for producto in productos_existentes:
            print(f"  - {producto}")
        
        print("\n" + "="*50 + "\n")
        
        # Agregar productos faltantes
        productos_agregados = 0
        productos_actualizados = 0
        
        for producto in productos_html:
            # Verificar si el producto ya existe
            cursor.execute('SELECT id FROM productos WHERE nombre = ? AND categoria = ?', 
                         (producto['nombre'], producto['categoria']))
            producto_existente = cursor.fetchone()
            
            if producto_existente:
                # Actualizar producto existente
                cursor.execute('''
                    UPDATE productos 
                    SET descripcion = ?, subcategoria = ?, precio = ?, precio_usd = ?, 
                        imagen_url = ?, imagen_mosaico_url = ?, activo = 1
                    WHERE id = ?
                ''', (
                    producto['descripcion'],
                    producto['subcategoria'],
                    producto['precio'],
                    producto['precio_usd'],
                    producto['imagen_url'],
                    producto['imagen_mosaico_url'],
                    producto_existente[0]
                ))
                productos_actualizados += 1
                print(f"✓ Actualizado: {producto['nombre']}")
            else:
                # Insertar nuevo producto
                cursor.execute('''
                    INSERT INTO productos (nombre, descripcion, categoria, subcategoria, 
                                         precio, precio_usd, imagen_url, 
                                         imagen_mosaico_url, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (
                    producto['nombre'],
                    producto['descripcion'],
                    producto['categoria'],
                    producto['subcategoria'],
                    producto['precio'],
                    producto['precio_usd'],
                    producto['imagen_url'],
                    producto['imagen_mosaico_url']
                ))
                productos_agregados += 1
                print(f"✓ Agregado: {producto['nombre']}")
        
        # Confirmar cambios
        conn.commit()
        
        print(f"\n" + "="*50)
        print(f"Resumen:")
        print(f"  - Productos agregados: {productos_agregados}")
        print(f"  - Productos actualizados: {productos_actualizados}")
        print(f"  - Total procesados: {len(productos_html)}")
        
        # Verificar resultado final
        cursor.execute('SELECT COUNT(*) FROM productos WHERE categoria = ? AND activo = 1', ('Piscinas',))
        total_final = cursor.fetchone()[0]
        print(f"  - Total activos en Piscinas: {total_final}")
        
        conn.close()
        print("\n✅ Proceso completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    agregar_productos_piscinas()
