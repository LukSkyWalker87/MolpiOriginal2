import os
import sqlite3
import shutil
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'molpi.db')


def backup_db(src_path: str) -> str:
    ts = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_dir = os.path.join(os.path.dirname(src_path), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    dst_path = os.path.join(backup_dir, f'molpi-backup-{ts}.db')
    shutil.copy2(src_path, dst_path)
    return dst_path


def ensure_unique_index(conn: sqlite3.Connection):
    cur = conn.cursor()
    # Índice único parcial: solo aplica a filas activas para permitir históricos inactivos
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS ux_subcategorias_unique_actives
        ON subcategorias (categoria_id, lower(trim(nombre)))
        WHERE activo = 1
        """
    )
    conn.commit()


def normalize(name: str) -> str:
    return (name or '').strip().lower()


def desactivar_duplicados(conn: sqlite3.Connection) -> int:
    cur = conn.cursor()
    # Buscar grupos duplicados entre las activas
    cur.execute(
        """
        SELECT categoria_id, lower(trim(nombre)) AS n, COUNT(*) AS cnt
        FROM subcategorias
        WHERE activo = 1
        GROUP BY categoria_id, n
        HAVING cnt > 1
        ORDER BY categoria_id, n
        """
    )
    grupos = cur.fetchall()

    total_desactivadas = 0
    for categoria_id, norm_name, _ in grupos:
        # Tomar una como canónica (la de menor id)
        cur.execute(
            """
            SELECT id, nombre
            FROM subcategorias
            WHERE categoria_id = ? AND lower(trim(nombre)) = ? AND activo = 1
            ORDER BY id ASC
            """,
            (categoria_id, norm_name),
        )
        filas = cur.fetchall()
        if not filas:
            continue
        keep_id = filas[0][0]
        # Desactivar el resto
        dup_ids = [fid for fid, _ in filas[1:]]
        if dup_ids:
            qmarks = ','.join('?' for _ in dup_ids)
            cur.execute(f"UPDATE subcategorias SET activo = 0 WHERE id IN ({qmarks})", dup_ids)
            total_desactivadas += len(dup_ids)

    conn.commit()
    return total_desactivadas


def main():
    if not os.path.exists(DB_PATH):
        raise SystemExit(f"No se encontró la base de datos en: {DB_PATH}")

    backup_path = backup_db(DB_PATH)
    print(f"✅ Backup creado: {backup_path}")

    conn = sqlite3.connect(DB_PATH)
    try:
        desact = desactivar_duplicados(conn)
        print(f"🧹 Subcategorías duplicadas desactivadas: {desact}")
        ensure_unique_index(conn)
        print("🔒 Índice único parcial asegurado: (categoria_id, lower(trim(nombre))) WHERE activo=1")
        # Reporte final rápido
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COUNT(*) FROM (
              SELECT categoria_id, lower(trim(nombre)) AS n, COUNT(*) AS cnt
              FROM subcategorias WHERE activo = 1
              GROUP BY categoria_id, n HAVING cnt > 1
            )
            """
        )
        pendientes = cur.fetchone()[0]
        if pendientes == 0:
            print("✅ No quedan duplicados activos por (categoria_id, nombre normalizado).")
        else:
            print(f"⚠️ Aún quedan {pendientes} grupos con duplicados activos.")
    finally:
        conn.close()


if __name__ == '__main__':
    main()
