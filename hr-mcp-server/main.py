# main.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from mcp.server.fastmcp import FastMCP
from tools.search import search_archive as _search_archive
from tools.documents import get_archive_detail as _get_archive_detail
from tools.staff_profiles import get_staff_profiles as _get_staff_profiles
from tools.file import get_file as _get_file
from tools.rag import rag_query as _rag_query
from config import settings

mcp = FastMCP("HR OCR MCP Server")


@mcp.tool()
def search_archive(
    keyword: str = None,
    status: str = None,
    maintenance: str = None,
    created_from: str = None,
    created_to: str = None,
    page: int = 0,
    size: int = 20,
) -> dict:
    """
    Tìm kiếm hồ sơ lưu trữ theo từ khóa, trạng thái, thời hạn bảo quản, ngày tạo.
    Hỗ trợ phân trang. Mỗi hồ sơ kèm staffMetadata, projects, borrowItems.
    Ví dụ: tìm theo tên cán bộ, mã hồ sơ, mã hộp, kho lưu trữ.
    """
    return _search_archive(
        keyword=keyword,
        status=status,
        maintenance=maintenance,
        created_from=created_from,
        created_to=created_to,
        page=page,
        size=size,
    )


@mcp.tool()
def get_archive_detail(archive_id: str) -> dict:
    """
    Lấy toàn bộ chi tiết 1 hồ sơ theo UUID.
    Trả về: thông tin cơ bản, staffMetadata (thông tin cán bộ),
    projects (dự án OCR + file), borrowItems (lịch sử mượn trả).
    """
    return _get_archive_detail(archive_id=archive_id)


@mcp.tool()
def get_staff_profiles(only_metadata: bool = False) -> dict:
    """
    Lấy danh sách hồ sơ cán bộ dạng JSON tĩnh.
    only_metadata=False: trả về đầy đủ kèm documentTypes.
    only_metadata=True : chỉ trả về thông tin cán bộ, bỏ documentTypes.
    """
    return _get_staff_profiles(only_metadata=only_metadata)


@mcp.tool()
def get_file(key: str, file_name: str = None) -> dict:
    """
    Lấy URL file (PDF, ảnh...) theo key từ storage.
    key lấy từ fileUrls trong projects của hồ sơ.
    Trả về URL để tải hoặc xem file.
    """
    return _get_file(key=key, file_name=file_name)


@mcp.tool()
def rag_query(query: str, top_k: int = 5) -> dict:
    """
    Tìm kiếm ngữ nghĩa trong toàn bộ tài liệu nhân viên bằng hybrid search.
    Dùng khi không biết chính xác tên hoặc ID, hoặc tìm theo nội dung.
    Ví dụ: tìm cán bộ có kinh nghiệm kế toán, ai có bằng thạc sĩ...
    """
    return _rag_query(query=query, top_k=top_k)


class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    """Yêu cầu header `Authorization: Bearer <MCP_API_KEY>` cho mọi request.

    Không có middleware này thì bất kỳ ai biết URL của server cũng gọi
    được tool và đọc dữ liệu hồ sơ nhân sự — bắt buộc bật khi deploy thật.
    """

    async def dispatch(self, request, call_next):
        auth = request.headers.get("authorization", "")
        expected = f"Bearer {settings.mcp_api_key}"
        if auth != expected:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)


def build_app():
    app = mcp.streamable_http_app()
    app.add_middleware(ApiKeyAuthMiddleware)
    return app


if __name__ == "__main__":
    import uvicorn
    from rag.embedder import get_model

    # Preload model bge-m3 lúc khởi động thay vì lúc có request rag_query
    # đầu tiên — tránh request đầu tiên bị timeout vì phải load model.
    print("Đang preload model bge-m3...")
    get_model()

    uvicorn.run(build_app(), host="0.0.0.0", port=8000)
