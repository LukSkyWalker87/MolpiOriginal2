#!/usr/bin/env python3
"""
Script para corregir rutas de imagen en la base de datos de promociones.
Cambia rutas que empiecen con 'car/img/promociones/' por 'img/promociones/'
"""

import sqlite3
import os

# Ruta a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')

def corregir_rutas_imagenes():
    """Corrige las rutas de imagen que tienen prefijo 'car/' """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Primero, ver qué rutas necesitan corrección
        cursor.execute("SELECT id, titulo, imagen FROM promociones WHERE imagen LIKE 'car/img/promociones/%'")
        rutas_incorrectas = cursor.fetchall()

        if not rutas_incorrectas:
            print("✅ No se encontraron rutas incorrectas. Todas las rutas están correctas.")
            return

        print(f"🔧 Se encontraron {len(rutas_incorrectas)} rutas incorrectas:")
        for row in rutas_incorrectas:
            print(f"  ID: {row[0]}, Título: {row[1]}, Ruta actual: {row[2]}")

        # Corregir las rutas
        cursor.execute("""
            UPDATE promociones
            SET imagen = REPLACE(imagen, 'car/img/promociones/', 'img/promociones/')
            WHERE imagen LIKE 'car/img/promociones/%'
        """)

        # Verificar que se corrigieron
        cursor.execute("SELECT COUNT(*) FROM promociones WHERE imagen LIKE 'car/img/promociones/%'")
        restantes = cursor.fetchone()[0]

        if restantes == 0:
            print("✅ Todas las rutas de imagen han sido corregidas exitosamente.")
        else:
            print(f"⚠️  Quedaron {restantes} rutas sin corregir.")

        conn.commit()

    except Exception as e:
        print(f"❌ Error corrigiendo rutas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 Corrigiendo rutas de imagen en promociones...")
    corregir_rutas_imagenes()
    print("✅ Proceso completado.")