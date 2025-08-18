import sqlite3
import os

db_files = [
    r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/backend/molpi.db',
    r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/OLD/molpi.db',
    r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/OLD/molpi_Python.db',
    r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/OLD/molpi_Python_instance.db',
    r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/OLD/molpi_backend.db',
]

for db_path in db_files:
    if not os.path.exists(db_path):
        print(f"NO EXISTE: {db_path}")
        continue
    print(f"\nAnalizando: {db_path}")
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in c.fetchall()]
        print("Tablas:", tables)
        if 'productos' in tables:
            c.execute("SELECT COUNT(*) FROM productos")
            count = c.fetchone()[0]
            print(f"  -> Tabla 'productos' encontrada. Registros: {count}")
            c.execute("SELECT id FROM productos LIMIT 10")
            ids = [row[0] for row in c.fetchall()]
            print(f"  -> Primeros IDs: {ids}")
        else:
            print("  -> Tabla 'productos' NO encontrada.")
        conn.close()
    except Exception as e:
        print(f"  -> ERROR: {e}")
