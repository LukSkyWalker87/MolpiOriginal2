#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def corregir_productos_40x40():
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    print('=== CORRIGIENDO PRODUCTOS LÍNEA 40x40 ===')
    
    # 1. Renombrar productos existentes
    renombramientos = [
        ('Cachada', 'Laja Cachada'),
        ('Laja San Luis', 'Laja San Luis N°1'),
        ('Laja San Luis 2', 'Laja San Luis N°2'),
        ('Laja San Luis 3', 'Laja San Luis N°3'),
        ('Laja Número 2 Octogonal', 'Laja N°2 Octogonal'),
        ('Lisa 40x40', 'Liso 40x40'),
        ('Liso 40', 'Liso con Bisel'),
        ('Octogonal 40x40', 'Octogonal'),
        ('Riojana 40x40', 'Riojana')
    ]
    
    print('\n--- RENOMBRANDO PRODUCTOS ---')
    for nombre_viejo, nombre_nuevo in renombramientos:
        cursor.execute('''
            UPDATE productos 
            SET nombre = ?, fecha_modificacion = ?
            WHERE nombre = ? AND subcategoria = 'Línea 40x40'
        ''', (nombre_nuevo, datetime.now(), nombre_viejo))
        
        if cursor.rowcount > 0:
            print(f'✅ {nombre_viejo} → {nombre_nuevo}')
        else:
            print(f'⚠️  {nombre_viejo} no encontrado')
    
    # 2. Eliminar productos que no pertenecen a la línea 40x40
    productos_eliminar = [
        'Adoquín Rústico',
        'Deck Símil Madera', 
        'Ladrillo Colonial',
        'Piedra París',
        'Plano 40x40'
    ]
    
    print('\n--- ELIMINANDO PRODUCTOS NO PERTENECIENTES ---')
    for producto in productos_eliminar:
        cursor.execute('''
            UPDATE productos 
            SET subcategoria = 'Otros', activo = 0
            WHERE nombre = ? AND subcategoria = 'Línea 40x40'
        ''', (producto,))
        
        if cursor.rowcount > 0:
            print(f'❌ {producto} movido a "Otros" y desactivado')
        else:
            print(f'⚠️  {producto} no encontrado en línea 40x40')
    
    # 3. Agregar productos faltantes
    productos_agregar = [
        {
            'nombre': 'Gregoriana',
            'descripcion': 'Molde para baldosa con diseño gregoriana 40x40cm.',
            'imagen_url': 'img/products/gregoriana_molde.jpg',
            'precio': 2200.0
        },
        {
            'nombre': 'Antideslizante',
            'descripcion': 'Molde para baldosa antideslizante 40x40cm.',
            'imagen_url': 'img/products/antideslizante_40x40_molde.jpg',
            'precio': 1750.0
        }
    ]
    
    print('\n--- AGREGANDO PRODUCTOS FALTANTES ---')
    for producto in productos_agregar:
        # Verificar si ya existe
        cursor.execute('SELECT id FROM productos WHERE nombre = ?', (producto['nombre'],))
        if cursor.fetchone():
            print(f'⚠️  {producto["nombre"]} ya existe')
            continue
            
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
                1,
                datetime.now(),
                datetime.now()
            ))
            print(f'✅ {producto["nombre"]} agregado')
            
        except sqlite3.IntegrityError as e:
            print(f'❌ Error agregando {producto["nombre"]}: {e}')
    
    # Confirmar cambios
    conn.commit()
    
    # Verificar resultado final
    cursor.execute('''
        SELECT COUNT(*) FROM productos 
        WHERE subcategoria = 'Línea 40x40' AND activo = 1
    ''')
    total = cursor.fetchone()[0]
    
    conn.close()
    
    print(f'\n🎉 Corrección completada. Total productos línea 40x40: {total}')
    return total

if __name__ == "__main__":
    corregir_productos_40x40()
