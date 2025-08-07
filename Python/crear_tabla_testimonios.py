#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la tabla de testimonios y precargar los datos existentes
"""

import sqlite3
import os

def crear_tabla_testimonios():
    """Crear la tabla de testimonios en la base de datos"""
    
    # Conectar a la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'molpi.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Crear tabla de testimonios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS testimonios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                empresa TEXT NOT NULL,
                testimonio TEXT NOT NULL,
                imagen TEXT DEFAULT 'img/clients/client-1.png',
                activo INTEGER DEFAULT 1,
                orden INTEGER DEFAULT 0,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Verificar si ya hay datos
        cursor.execute('SELECT COUNT(*) FROM testimonios')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Precargar los testimonios existentes de la página
            testimonios_iniciales = [
                {
                    'nombre': 'Carlos Rodríguez',
                    'empresa': 'Constructora Edificar',
                    'testimonio': 'Los moldes para baldosas de Molpi superaron ampliamente nuestras expectativas. El diseño autoestibable nos permitió optimizar considerablemente el espacio en nuestro taller.',
                    'imagen': 'img/clients/client-1.png',
                    'orden': 1
                },
                {
                    'nombre': 'Juan López',
                    'empresa': 'Pisos & Revestimientos SRL',
                    'testimonio': 'Comenzamos con un pequeño emprendimiento y el asesoramiento de Molpi fue clave para nuestro crecimiento. La durabilidad de sus moldes es incomparable en el mercado.',
                    'imagen': 'img/clients/client-1.png',
                    'orden': 2
                },
                {
                    'nombre': 'Gabriel Méndez',
                    'empresa': 'Urbana Construcciones',
                    'testimonio': 'La línea de moldes podotáctiles nos permitió expandir nuestro negocio hacia proyectos municipales. La calidad y precisión del producto final es excelente.',
                    'imagen': 'img/clients/client-1.png',
                    'orden': 3
                }
            ]
            
            # Insertar testimonios iniciales
            for testimonio in testimonios_iniciales:
                cursor.execute('''
                    INSERT INTO testimonios (nombre, empresa, testimonio, imagen, orden)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    testimonio['nombre'],
                    testimonio['empresa'],
                    testimonio['testimonio'],
                    testimonio['imagen'],
                    testimonio['orden']
                ))
            
            print(f"✅ Tabla 'testimonios' creada y precargada con {len(testimonios_iniciales)} testimonios")
        else:
            print(f"✅ Tabla 'testimonios' ya existe con {count} registros")
        
        conn.commit()
        
        # Mostrar testimonios existentes
        cursor.execute('SELECT id, nombre, empresa FROM testimonios ORDER BY orden')
        testimonios = cursor.fetchall()
        
        print("\n📝 Testimonios en la base de datos:")
        for testimonio in testimonios:
            print(f"  {testimonio[0]}. {testimonio[1]} - {testimonio[2]}")
            
    except Exception as e:
        print(f"❌ Error al crear tabla de testimonios: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    crear_tabla_testimonios()
