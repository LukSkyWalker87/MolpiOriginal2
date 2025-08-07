#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def agregar_productos_40x40():
    # Lista de productos faltantes para la línea 40x40
    productos_40x40 = [
        {
            'nombre': 'Plano 40x40',
            'descripcion': 'Molde para baldosa plana 40x40cm.',
            'imagen_url': 'img/products/plano_40x40_molde.jpg',
            'precio': 2000.0
        },
        {
            'nombre': 'Adoquín Curvo Chico',
            'descripcion': 'Molde para baldosa con diseño de adoquín curvo chico.',
            'imagen_url': 'img/products/adoquin_curvo_chico_molde.jpg',
            'precio': 1850.0
        },
        {
            'nombre': 'Adoquín Curvo Grande',
            'descripcion': 'Molde para baldosa con diseño de adoquín curvo grande.',
            'imagen_url': 'img/products/adoquin_curvo_grande_molde.jpg',
            'precio': 1900.0
        },
        {
            'nombre': 'Adoquín Recto Chico',
            'descripcion': 'Molde para baldosa con diseño de adoquín recto chico.',
            'imagen_url': 'img/products/adoquin_recto_chico_molde.jpg',
            'precio': 1800.0
        },
        {
            'nombre': 'Adoquín Recto Grande',
            'descripcion': 'Molde para baldosa con diseño de adoquín recto grande.',
            'imagen_url': 'img/products/adoquin_recto_grande_molde.jpg',
            'precio': 1850.0
        },
        {
            'nombre': 'Laja Española',
            'descripcion': 'Molde para baldosa con diseño laja española.',
            'imagen_url': 'img/products/laja_espanola_molde.jpg',
            'precio': 2100.0
        },
        {
            'nombre': 'Laja Ladrillo',
            'descripcion': 'Molde para baldosa con diseño laja ladrillo.',
            'imagen_url': 'img/products/laja_ladrillo_molde.jpg',
            'precio': 2050.0
        },
        {
            'nombre': 'Laja San Luis',
            'descripcion': 'Molde para baldosa con diseño laja San Luis.',
            'imagen_url': 'img/products/laja_san_luis_molde.jpg',
            'precio': 2150.0
        },
        {
            'nombre': 'Laja San Luis 2',
            'descripcion': 'Molde para baldosa con diseño laja San Luis versión 2.',
            'imagen_url': 'img/products/laja_san_luis_2_molde.jpg',
            'precio': 2150.0
        },
        {
            'nombre': 'Laja San Luis 3',
            'descripcion': 'Molde para baldosa con diseño laja San Luis versión 3.',
            'imagen_url': 'img/products/laja_san_luis_3_molde.jpg',
            'precio': 2150.0
        },
        {
            'nombre': 'Cachada',
            'descripcion': 'Molde para baldosa con diseño cachada.',
            'imagen_url': 'img/products/cachada_molde.jpg',
            'precio': 1950.0
        },
        {
            'nombre': 'Laja Número 2 Octogonal',
            'descripcion': 'Molde para baldosa con diseño laja número 2 octogonal.',
            'imagen_url': 'img/products/laja_n2_octogonal_molde.jpg',
            'precio': 2200.0
        },
        {
            'nombre': 'Laja San Pedro',
            'descripcion': 'Molde para baldosa con diseño laja San Pedro.',
            'imagen_url': 'img/products/laja_san_pedro_molde.jpg',
            'precio': 2100.0
        },
        {
            'nombre': 'Riojana con Bisel',
            'descripcion': 'Molde para baldosa riojana con bisel 40x40cm.',
            'imagen_url': 'img/products/riojana_bisel_molde.jpg',
            'precio': 2250.0
        },
        {
            'nombre': 'Travertino Viejo',
            'descripcion': 'Molde para baldosa con diseño travertino viejo.',
            'imagen_url': 'img/products/travertino_viejo_molde.jpg',
            'precio': 2300.0
        },
        {
            'nombre': 'Liso 40',
            'descripcion': 'Molde para baldosa lisa 40x40cm.',
            'imagen_url': 'img/products/liso_40_molde.jpg',
            'precio': 1900.0
        },
        {
            'nombre': 'Lisa con Bisel',
            'descripcion': 'Molde para baldosa lisa con bisel 40x40cm.',
            'imagen_url': 'img/products/lisa_bisel_molde.jpg',
            'precio': 2000.0
        },
        {
            'nombre': '64 Panes',
            'descripcion': 'Molde para baldosa con diseño 64 panes.',
            'imagen_url': 'img/products/64_panes_molde.jpg',
            'precio': 2400.0
        },
        {
            'nombre': 'Curvo Chico Liso',
            'descripcion': 'Molde para baldosa con diseño curvo chico liso.',
            'imagen_url': 'img/products/curvo_chico_liso_molde.jpg',
            'precio': 1900.0
        },
        {
            'nombre': 'Guarda',
            'descripcion': 'Molde para baldosa con diseño guarda.',
            'imagen_url': 'img/products/guarda_molde.jpg',
            'precio': 2050.0
        },
        {
            'nombre': 'Zócalo Lineal',
            'descripcion': 'Molde para zócalo lineal 40x40cm.',
            'imagen_url': 'img/products/zocalo_lineal_molde.jpg',
            'precio': 1800.0
        },
        {
            'nombre': 'Zócalo Incaico',
            'descripcion': 'Molde para zócalo incaico 40x40cm.',
            'imagen_url': 'img/products/zocalo_incaico_molde.jpg',
            'precio': 1950.0
        }
    ]
    
    # Conectar a la base de datos
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    # Agregar cada producto
    productos_agregados = 0
    for producto in productos_40x40:
        try:
            cursor.execute('''
                INSERT INTO productos (
                    nombre, descripcion, imagen_url, categoria, subcategoria, 
                    precio, activo, fecha_creacion, fecha_modificacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                producto['nombre'],
                producto['descripcion'], 
                producto['imagen_url'],
                'Pisos y Zócalos',
                'Línea 40x40',
                producto['precio'],
                1,  # activo
                datetime.now(),
                datetime.now()
            ))
            productos_agregados += 1
            print(f"✅ Agregado: {producto['nombre']}")
            
        except sqlite3.IntegrityError as e:
            print(f"⚠️  Ya existe o error: {producto['nombre']} - {e}")
        except Exception as e:
            print(f"❌ Error: {producto['nombre']} - {e}")
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Proceso completado: {productos_agregados} productos agregados a la línea 40x40")
    
    return productos_agregados

if __name__ == "__main__":
    agregar_productos_40x40()
