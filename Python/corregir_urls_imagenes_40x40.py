#!/usr/bin/env python3
import sqlite3

def actualizar_urls_imagen():
    conn = sqlite3.connect('molpi.db')
    cursor = conn.cursor()
    
    # Correcciones de URLs de imagen
    correcciones = [
        ('Laja Número 2 Octogonal', 'img/products/laja_numero_2_octogonal_molde.jpg'),
        ('Lisa con Bisel', 'img/products/lisa_con_bisel_molde.jpg'),
        ('Plano 40x40', 'img/products/plano_40x40.png'),
        ('Riojana con Bisel', 'img/products/riojana_con_bisel_molde.jpg')
    ]
    
    print('=== ACTUALIZANDO URLS DE IMAGEN ===')
    actualizaciones = 0
    
    for nombre, nueva_url in correcciones:
        cursor.execute('''
            UPDATE productos 
            SET imagen_url = ? 
            WHERE nombre = ?
        ''', (nueva_url, nombre))
        
        if cursor.rowcount > 0:
            print(f'✅ {nombre:<25} -> {nueva_url}')
            actualizaciones += 1
        else:
            print(f'❌ {nombre:<25} -> NO ENCONTRADO')
    
    # Confirmar cambios
    conn.commit()
    conn.close()
    
    print(f'\n🎉 {actualizaciones} URLs de imagen actualizadas correctamente')
    return actualizaciones

if __name__ == "__main__":
    actualizar_urls_imagen()
