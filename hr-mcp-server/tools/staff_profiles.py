# tools/staff_profiles.py
"""
Tool: get_staff_profiles
UC10: Lấy danh sách toàn bộ hồ sơ cán bộ kèm tài liệu
UC11: Lấy chỉ metadata cán bộ (không kèm documentTypes)
"""
import httpx

from config import settings


def get_staff_profiles(only_metadata: bool = False) -> dict:
    try:
        with httpx.Client(timeout=30) as client:
            r = client.get(
                settings.staff_profile_api_url,
                params={"only_metadata": str(only_metadata).lower()},
            )
        if r.status_code != 200:
            return {"error": f"API lỗi: {r.status_code}"}
        return {"data": r.json()}
    except httpx.RequestError as e:
        return {"error": f"Không kết nối được tới Staff Profile API: {e}"}
    except Exception as e:
        return {"error": str(e)}
