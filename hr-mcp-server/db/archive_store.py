# db/archive_store.py
import psycopg2
from psycopg2 import pool

from config import settings

# Connection pool dùng chung — tránh mở/đóng connection mới mỗi lần upsert
_pool = None


def _get_pool():
    global _pool
    if _pool is None:
        _pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1, maxconn=10, dsn=settings.postgres_url
        )
    return _pool


def get_conn():
    """Lấy 1 connection từ pool. Nhớ gọi release_conn(conn) sau khi dùng xong."""
    return _get_pool().getconn()


def release_conn(conn):
    _get_pool().putconn(conn)


def upsert_archive(archive: dict):
    """Thêm mới hoặc cập nhật 1 archive vào PostgreSQL"""
    meta = archive.get("staff_metadata") or {}
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO archives (
                    id, title, arc_file_code, status,
                    start_date, end_date, maintenance,
                    ho_va_ten, ngay_sinh, don_vi_cong_tac, dia_chi, chuc_vu,
                    synced_at
                ) VALUES (
                    %(id)s, %(title)s, %(arc_file_code)s, %(status)s,
                    %(start_date)s, %(end_date)s, %(maintenance)s,
                    %(ho_va_ten)s, %(ngay_sinh)s, %(don_vi_cong_tac)s, %(dia_chi)s, %(chuc_vu)s,
                    NOW()
                )
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    arc_file_code = EXCLUDED.arc_file_code,
                    status = EXCLUDED.status,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    maintenance = EXCLUDED.maintenance,
                    ho_va_ten = EXCLUDED.ho_va_ten,
                    ngay_sinh = EXCLUDED.ngay_sinh,
                    don_vi_cong_tac = EXCLUDED.don_vi_cong_tac,
                    dia_chi = EXCLUDED.dia_chi,
                    chuc_vu = EXCLUDED.chuc_vu,
                    synced_at = NOW()
                """,
                {
                    "id": archive["id"],
                    "title": archive.get("title"),
                    "arc_file_code": archive.get("arc_file_code"),
                    "status": archive.get("status"),
                    "start_date": archive.get("start_date"),
                    "end_date": archive.get("end_date"),
                    "maintenance": archive.get("maintenance"),
                    "ho_va_ten": meta.get("ho_va_ten"),
                    "ngay_sinh": meta.get("ngay_sinh"),
                    "don_vi_cong_tac": meta.get("don_vi_cong_tac"),
                    "dia_chi": meta.get("dia_chi"),
                    "chuc_vu": meta.get("chuc_vu"),
                },
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        release_conn(conn)
