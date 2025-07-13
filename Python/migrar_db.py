import sqlite3
import os

def migrar_base_datos():
    conn = sqlite3.connect('molpi.db')
    c = conn.cursor()
    
    print("Iniciando migración de base de datos...")
    
    # Verificar si la tabla productos tiene las nuevas columnas
    c.execute("PRAGMA table_info(productos)")
    columns = [col[1] for col in c.fetchall()]
    
    nuevas_columnas = [
        ('categoria', 'TEXT NOT NULL DEFAULT ""'),
        ('subcategoria', 'TEXT NOT NULL DEFAULT ""'),
        ('precio', 'REAL DEFAULT 0'),
        ('activo', 'INTEGER DEFAULT 1'),
        ('fecha_creacion', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'),
        ('fecha_modificacion', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    ]
    
    # Agregar columnas que no existen
    for columna, tipo in nuevas_columnas:
        if columna not in columns:
            try:
                c.execute(f"ALTER TABLE productos ADD COLUMN {columna} {tipo}")
                print(f"✅ Columna '{columna}' agregada a la tabla productos")
            except Exception as e:
                print(f"❌ Error agregando columna '{columna}': {e}")
    
    # Verificar si necesitamos crear las demás tablas
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas_existentes = [tabla[0] for tabla in c.fetchall()]
    
    # Crear tabla categorias si no existe
    if 'categorias' not in tablas_existentes:
        c.execute("""
            CREATE TABLE categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                descripcion TEXT,
                activo INTEGER DEFAULT 1
            )
        """)
        print("✅ Tabla 'categorias' creada")
    
    # Crear tabla subcategorias si no existe
    if 'subcategorias' not in tablas_existentes:
        c.execute("""
            CREATE TABLE subcategorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria_id INTEGER,
                descripcion TEXT,
                activo INTEGER DEFAULT 1,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        """)
        print("✅ Tabla 'subcategorias' creada")
    
    # Crear tabla producto_imagenes si no existe
    if 'producto_imagenes' not in tablas_existentes:
        c.execute("""
            CREATE TABLE producto_imagenes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER,
                imagen_url TEXT,
                orden INTEGER DEFAULT 0,
                FOREIGN KEY (producto_id) REFERENCES productos (id)
            )
        """)
        print("✅ Tabla 'producto_imagenes' creada")
    
    # Insertar categorías por defecto
    categorias_default = [
        ('Pisos y Zócalos', 'Moldes para baldosas lisas o rústicas para interiores y exteriores'),
        ('Revestimientos', 'Moldes para revestimientos símil piedra o madera'),
        ('Podotáctiles - Discapacidad', 'Moldes para baldosas destinadas a señalización urbana'),
        ('Green', 'Moldes ecológicos y sustentables'),
        ('Piscinas', 'Moldes específicos para áreas de piscinas'),
        ('Placas Antihumedad', 'Moldes para placas contra la humedad'),
        ('Insumos', 'Materiales y herramientas complementarias')
    ]
    
    for categoria, desc in categorias_default:
        try:
            c.execute("INSERT OR IGNORE INTO categorias (nombre, descripcion) VALUES (?, ?)", (categoria, desc))
        except Exception as e:
            print(f"Error insertando categoría '{categoria}': {e}")
    
    # Insertar subcategorías por defecto
    subcategorias_default = [
        ('Línea 20x20', 1),
        ('Línea 40x40', 1),
        ('Línea 50x50', 1),
        ('Revestimientos Piedra', 2),
        ('Revestimientos Madera', 2),
        ('Señalización', 3),
        ('Guías Táctiles', 3),
        ('Eco-Moldes', 4),
        ('Bordes Piscina', 5),
        ('Placas Estándar', 6),
        ('Desmoldantes', 7),
        ('Pigmentos', 7)
    ]
    
    for subcategoria, cat_id in subcategorias_default:
        try:
            c.execute("INSERT OR IGNORE INTO subcategorias (nombre, categoria_id) VALUES (?, ?)", (subcategoria, cat_id))
        except Exception as e:
            print(f"Error insertando subcategoría '{subcategoria}': {e}")
    
    # Insertar algunos productos de ejemplo para la línea 20x20
    productos_ejemplo = [
        ('Vainilla de 5', 'Molde para baldosas con diseño vainilla de 5 cm', 'Pisos y Zócalos', 'Línea 20x20', 'img/products/vainilla5.jpg', 'pdf/vainilla5.pdf', 1500.00),
        ('Vainilla de 6', 'Molde para baldosas con diseño vainilla de 6 cm', 'Pisos y Zócalos', 'Línea 20x20', 'img/products/vainilla6.jpg', 'pdf/vainilla6.pdf', 1650.00),
        ('Adoquín Rústico', 'Molde para baldosas con diseño de adoquín rústico', 'Pisos y Zócalos', 'Línea 20x20', 'img/products/adoquin.jpg', 'pdf/adoquin.pdf', 1800.00),
        ('Piedra París', 'Molde para baldosas con diseño símil piedra París', 'Pisos y Zócalos', 'Línea 20x20', 'img/products/piedra_paris.jpg', 'pdf/piedra_paris.pdf', 1750.00)
    ]
    
    for nombre, desc, categoria, subcategoria, imagen, pdf, precio in productos_ejemplo:
        try:
            c.execute("""
                INSERT OR IGNORE INTO productos (nombre, descripcion, categoria, subcategoria, imagen_url, pdf_url, precio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, desc, categoria, subcategoria, imagen, pdf, precio))
        except Exception as e:
            print(f"Error insertando producto '{nombre}': {e}")
    
    conn.commit()
    print("✅ Migración completada")
    
    # Mostrar estadísticas finales
    c.execute("SELECT COUNT(*) FROM categorias")
    cat_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM subcategorias")
    sub_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM productos")
    prod_count = c.fetchone()[0]
    
    print(f"\nEstadísticas finales:")
    print(f"  Categorías: {cat_count}")
    print(f"  Subcategorías: {sub_count}")
    print(f"  Productos: {prod_count}")
    
    conn.close()

if __name__ == "__main__":
    migrar_base_datos()
