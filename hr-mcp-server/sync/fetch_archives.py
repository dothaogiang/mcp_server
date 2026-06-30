# sync/fetch_archives.py
import httpx

from config import settings
from db.archive_store import upsert_archive
from rag.pipeline import index_document, create_collection


def sync_all_archives(reindex_rag: bool = True):
    """Kéo toàn bộ archive từ Search API, upsert vào PostgreSQL,
    đồng thời (mặc định) index nội dung vào Qdrant để rag_query dùng được.
    """
    print("Bắt đầu sync archives...")

    if reindex_rag:
        create_collection()

    with httpx.Client(timeout=30) as client:
        response = client.get(settings.search_api_url)
        response.raise_for_status()
        data = response.json()

    archives = data.get("data", data.get("content", []))
    ok, failed = 0, 0

    for archive in archives:
        archive_id = archive.get("id")
        if not archive_id:
            print(f"  ✗ Bỏ qua 1 archive thiếu 'id': {archive}")
            failed += 1
            continue
        try:
            upsert_archive(archive)
            if reindex_rag:
                index_document(archive_id, archive)
            ok += 1
            print(f"  ✓ Synced: {archive_id} — {archive.get('title')}")
        except Exception as e:
            failed += 1
            print(f"  ✗ Lỗi khi sync {archive_id}: {e}")

    print(f"Xong! Thành công: {ok}, lỗi: {failed}, tổng: {len(archives)} archives.")


if __name__ == "__main__":
    sync_all_archives()
