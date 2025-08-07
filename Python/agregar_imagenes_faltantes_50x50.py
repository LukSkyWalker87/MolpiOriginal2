#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def copiar_imagenes_faltantes():
    """
    Copia imágenes existentes para crear las imágenes faltantes de productos 50x50
    """
    
    # Directorio base de imágenes
    img_dir = "../www.molpi.com.ar/img/products/"
    
    # Mapeo de imágenes faltantes con sus equivalentes existentes
    copias_necesarias = {
        # Imagen faltante : Imagen existente que usaremos
        "adoquín_colonial_molde.jpg": "adoquin_individual_molde.jpg",
        "deck_antideslizante_molde.jpg": "deckmadera_antideslizante_molde.jpg", 
        "deck_símil_madera_molde.jpg": "deck_simil_madera_molde.jpg",
        "liso_molde.jpg": "liso_40_molde.jpg",
        "madera_50x25x6___2_piezas_por_molde_molde.jpg": "madera_6_cm_molde.jpg"
    }
    
    print("=== AGREGANDO IMÁGENES FALTANTES PARA PRODUCTOS 50x50 ===\n")
    
    for imagen_faltante, imagen_origen in copias_necesarias.items():
        origen_path = os.path.join(img_dir, imagen_origen)
        destino_path = os.path.join(img_dir, imagen_faltante)
        
        print(f"Procesando: {imagen_faltante}")
        
        # Verificar si la imagen origen existe
        if not os.path.exists(origen_path):
            print(f"  ❌ ERROR: La imagen origen no existe: {imagen_origen}")
            continue
            
        # Verificar si la imagen destino ya existe
        if os.path.exists(destino_path):
            print(f"  ⚠️  La imagen ya existe: {imagen_faltante}")
            continue
            
        try:
            # Copiar la imagen
            shutil.copy2(origen_path, destino_path)
            print(f"  ✅ Copiada: {imagen_origen} → {imagen_faltante}")
            
        except Exception as e:
            print(f"  ❌ Error al copiar {imagen_origen}: {str(e)}")
    
    print("\n=== VERIFICACIÓN FINAL ===")
    
    # Verificar que todas las imágenes ahora existen
    for imagen_faltante in copias_necesarias.keys():
        destino_path = os.path.join(img_dir, imagen_faltante)
        if os.path.exists(destino_path):
            print(f"✅ {imagen_faltante} - EXISTE")
        else:
            print(f"❌ {imagen_faltante} - NO EXISTE")

if __name__ == "__main__":
    copiar_imagenes_faltantes()
