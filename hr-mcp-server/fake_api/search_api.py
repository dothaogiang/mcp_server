# fake_api/search_api.py
from fastapi import FastAPI, Query
from fake_api.mock_data import FAKE_ARCHIVES, FAKE_STAFF_PROFILES
from typing import Optional

app = FastAPI(title="Fake HR API")


# ── 1. Tìm kiếm hồ sơ (UC01-UC05) ────────────────────────────────
@app.get("/api/public/archives")
def search_archives(
    keyword: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    maintenance: Optional[str] = Query(None),
    createdFrom: Optional[str] = Query(None),
    createdTo: Optional[str] = Query(None),
    page: int = Query(0),
    size: int = Query(20),
):
    results = FAKE_ARCHIVES

    if keyword:
        kw = keyword.lower()
        results = [
            a for a in results
            if kw in a.get("title", "").lower()
            or kw in (a.get("arcFileCode") or a.get("arc_file_code") or "").lower()
            or kw in (a.get("boxCode") or a.get("box_code") or "").lower()
            or any(kw in m["value"].lower() for m in a.get("staffMetadata", []))
        ]

    if status:
        results = [a for a in results if a.get("status") == status.upper()]

    if maintenance:
        results = [a for a in results if a.get("maintenance") == maintenance]

    if createdFrom:
        results = [a for a in results if (a.get("createdAt") or "")[:10] >= createdFrom]

    if createdTo:
        results = [a for a in results if (a.get("createdAt") or "")[:10] <= createdTo]

    total = len(results)
    start = page * size
    end = start + size
    paged = results[start:end]

    return {
        "totalPages": (total + size - 1) // size,
        "totalElements": total,
        "size": size,
        "number": page,
        "first": page == 0,
        "last": end >= total,
        "numberOfElements": len(paged),
        "content": paged,
    }

# ── 2. Chi tiết hồ sơ theo ID (UC06-UC09) ─────────────────────────
@app.get("/api/public/archives/{id}")
def get_archive_by_id(id: str):
    for a in FAKE_ARCHIVES:
        if a["id"] == id:
            return a
    return {"status": 404, "message": "Không tìm thấy hồ sơ với ID này"}


# ── 3. Danh sách hồ sơ cán bộ (UC10-UC11) ─────────────────────────
@app.get("/api/public/staff-profiles")
def get_staff_profiles(only_metadata: bool = Query(False)):
    if only_metadata:
        # Bỏ trường documentTypes
        return [
            {k: v for k, v in p.items() if k != "documentTypes"}
            for p in FAKE_STAFF_PROFILES
        ]
    return FAKE_STAFF_PROFILES


# ── 4. Lấy file theo key (UC15) ────────────────────────────────────
@app.get("/api/public/files/proxy")
def get_file(key: str = Query(...), fileName: Optional[str] = Query(None)):
    # Fake trả về URL giả lập
    return f"http://localhost:8001/static/{key}"