#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

def crear_imagenes_mosaico_faltantes_50x50():
    """
    Crea las imágenes de mosaico faltantes para productos 50x50
    """
    
    img_dir = "../www.molpi.com.ar/img/products/"
    
    # Mapeo de imágenes faltantes con sus equivalentes existentes
    copias_necesarias = {
        # Deck Antideslizante - usar la imagen que mencionaste
        "deck_antideslizante_mosaico.png": "deckmadera_antideslizante_mosaico.png",
        # Liso - usar liso_50_mosaico.png que ya existe
        "liso_mosaico.png": "liso_50_mosaico.png"
    }
    
    print("=== CREANDO IMÁGENES DE MOSAICO FALTANTES PARA 50x50 ===\n")
    
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
    
    # Verificar que todas las imágenes de mosaico ahora existan
    productos_50x50 = [
        ("Laja San Juan", "laja_san_juan_mosaico.png"),
        ("Adoquín Colonial", "laja_colonial_mosaico.png"), 
        ("Deck Símil Madera", "deck_simil_madera_mosaico.png"),
        ("Deck Antideslizante", "deck_antideslizante_mosaico.png"),
        ("Madera 50x25x6", "madera_6_cm_mosaico.png"),
        ("Liso", "liso_mosaico.png"),
        ("Quebracho", "quebracho_mosaico.png"),
        ("Corteza", "corteza_mosaico.png")
    ]
    
    for nombre, imagen_mosaico in productos_50x50:
        mosaico_path = os.path.join(img_dir, imagen_mosaico)
        if os.path.exists(mosaico_path):
            print(f"✅ {nombre:25s} | {imagen_mosaico}")
        else:
            print(f"❌ {nombre:25s} | {imagen_mosaico} - NO EXISTE")

if __name__ == "__main__":
    crear_imagenes_mosaico_faltantes_50x50()
