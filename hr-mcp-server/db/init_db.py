# db/init_db.py
import psycopg2

from config import settings


def init():
    conn = psycopg2.connect(settings.postgres_url)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS archives (
            id TEXT PRIMARY KEY,
            title TEXT,
            arc_file_code TEXT,
            status TEXT,
            start_date TEXT,
            end_date TEXT,
            maintenance TEXT,
            ho_va_ten TEXT,
            ngay_sinh TEXT,
            don_vi_cong_tac TEXT,
            dia_chi TEXT,
            chuc_vu TEXT,
            synced_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
    )
    cur.execute("CREATE INDEX IF NOT EXISTS idx_archives_status ON archives(status);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_archives_ho_va_ten ON archives(ho_va_ten);")

    conn.commit()
    cur.close()
    conn.close()
    print("Tạo bảng thành công!")


if __name__ == "__main__":
    init()
