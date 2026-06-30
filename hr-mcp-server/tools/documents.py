# tools/documents.py
"""
Tool: get_archive_detail
UC06: Lấy chi tiết hồ sơ theo ID
UC07: Xem staffMetadata của hồ sơ
UC08: Xem projects + fileUrls (đã OCR chưa, có file gì)
UC09: Xem borrowItems (lịch sử mượn)
"""
import httpx

from config import settings


def get_archive_detail(archive_id: str) -> dict:
    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(f"{settings.document_api_url}/{archive_id}")
        if r.status_code == 404:
            return {"error": f"Không tìm thấy hồ sơ: {archive_id}"}
        if r.status_code != 200:
            return {"error": f"API lỗi: {r.status_code}"}
        return r.json()
    except httpx.RequestError as e:
        return {"error": f"Không kết nối được tới Document API: {e}"}
    except Exception as e:
        return {"error": str(e)}
