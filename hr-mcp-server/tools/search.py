# tools/search.py
"""
Tool: search_archive
UC01: Tìm hồ sơ theo từ khóa (tên, mã hồ sơ, mã hộp)
UC02: Lọc theo trạng thái (PENDING, PROCESSING, COMPLETED)
UC03: Lọc theo ngày tạo
UC04: Lọc theo kho lưu trữ
UC05: Lọc theo thời hạn bảo quản
"""
import httpx

from config import settings


def search_archive(
    keyword: str = None,
    status: str = None,
    maintenance: str = None,
    created_from: str = None,
    created_to: str = None,
    page: int = 0,
    size: int = 20,
) -> dict:
    params = {"page": page, "size": size}
    if keyword: params["keyword"] = keyword
    if status: params["status"] = status
    if maintenance: params["maintenance"] = maintenance
    if created_from: params["createdFrom"] = created_from
    if created_to: params["createdTo"] = created_to

    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(settings.search_api_url, params=params)
        if r.status_code != 200:
            return {"error": f"API lỗi: {r.status_code}"}
        return r.json()
    except httpx.RequestError as e:
        return {"error": f"Không kết nối được tới Search API: {e}"}
    except Exception as e:
        return {"error": str(e)}
