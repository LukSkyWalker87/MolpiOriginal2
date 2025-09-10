import sqlite3
from collections import defaultdict

DB_PATH = r'c:/Users/lucas/OneDrive/Documentos/GitHub/molpioriginal3/MolpiOriginal2/backend/molpi.db'

def normalize(name: str) -> str:
    return (name or '').strip().lower()

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Traer subcategorías con su categoría
    c.execute(
        """
        SELECT s.id, s.nombre, s.categoria_id, s.descripcion, s.activo, c.nombre as categoria
        FROM subcategorias s
        LEFT JOIN categorias c ON c.id = s.categoria_id
        ORDER BY c.nombre, s.nombre
        """
    )
    rows = c.fetchall()
    conn.close()

    print(f"Total subcategorías: {len(rows)}\n")
    by_cat = defaultdict(list)
    for rid, sname, cid, desc, activo, catname in rows:
        by_cat[(cid, catname)].append((rid, sname, activo))

    dup_total = 0
    for (cid, catname), items in by_cat.items():
        seen = defaultdict(list)
        for rid, sname, activo in items:
            seen[normalize(sname)].append((rid, sname, activo))
        dups = {k:v for k,v in seen.items() if len(v) > 1}
        if dups:
            print(f"Categoria [{cid}] {catname} -> DUPLICADOS:")
            for key, lst in dups.items():
                dup_total += len(lst)
                for rid, sname, activo in lst:
                    print(f"  - id={rid} nombre='{sname}' activo={activo}")
            print()

    if dup_total == 0:
        print("No se detectaron duplicados por (categoria_id, nombre).")

if __name__ == '__main__':
    main()
