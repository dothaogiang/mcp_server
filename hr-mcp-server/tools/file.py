# tools/file.py
"""
Tool: get_file
UC15: Lấy URL file PDF của hồ sơ theo key
"""
import httpx

from config import settings


def get_file(key: str, file_name: str = None) -> dict:
    try:
        params = {"key": key}
        if file_name:
            params["fileName"] = file_name
        with httpx.Client(timeout=30) as client:
            r = client.get(settings.file_api_url, params=params)
        if r.status_code != 200:
            return {"error": f"API lỗi: {r.status_code}"}
        return {"url": r.text}
    except httpx.RequestError as e:
        return {"error": f"Không kết nối được tới File API: {e}"}
    except Exception as e:
        return {"error": str(e)}
