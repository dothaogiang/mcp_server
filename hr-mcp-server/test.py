# test_tools.py
import httpx, json

BASE = "http://localhost:8000/mcp"
HEADERS_INIT = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# Khởi tạo session
r = httpx.post(BASE, headers=HEADERS_INIT, json={
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2024-11-05", "clientInfo": {"name": "test", "version": "1.0"}, "capabilities": {}}
})
SESSION_ID = r.headers.get("mcp-session-id")
HEADERS = {**HEADERS_INIT, "mcp-session-id": SESSION_ID}

def call_tool(name, args):
    r = httpx.post(BASE, headers=HEADERS, json={
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": name, "arguments": args}
    }, timeout=60)
    data = json.loads(r.text.split("data: ")[1])
    result = json.loads(data["result"]["content"][0]["text"])
    return result

print("\n── UC01: Tìm hồ sơ theo từ khóa ──")
r1 = call_tool("search_archive", {"keyword": "An"})
print(f"Tìm thấy: {r1['totalElements']} hồ sơ")
print(f"Tiêu đề: {r1['content'][0]['title']}")

print("\n── UC02: Lọc theo trạng thái ──")
r2 = call_tool("search_archive", {"status": "PROCESSING"})
print(f"Đang xử lý: {r2['totalElements']} hồ sơ")

print("\n── UC06: Lấy chi tiết hồ sơ ──")
r3 = call_tool("get_archive_detail", {"archive_id": "a1b2c3d4-0001-0000-0000-000000000001"})
print(f"Hồ sơ: {r3['title']}")
print(f"Metadata: {[m['fieldName'] for m in r3['staffMetadata']]}")

print("\n── UC09: Xem lịch sử mượn ──")
r4 = call_tool("get_archive_detail", {"archive_id": "a1b2c3d4-0002-0000-0000-000000000002"})
print(f"Số lần mượn: {len(r4['borrowItems'])}")

print("\n── UC10: Danh sách hồ sơ cán bộ ──")
r5 = call_tool("get_staff_profiles", {"only_metadata": False})
print(f"Tổng cán bộ: {len(r5['data'])}")

print("\n── UC11: Chỉ metadata cán bộ ──")
r6 = call_tool("get_staff_profiles", {"only_metadata": True})
print(f"Có documentTypes không: {'documentTypes' in r6['data'][0]}")

print("\n── UC15: Lấy file ──")
r7 = call_tool("get_file", {"key": "files/nguyen-van-an/ly-lich.pdf"})
print(f"URL file: {r7['url']}")

print("\n── UC12: RAG query ──")
r8 = call_tool("rag_query", {"query": "kỹ sư Hà Nội"})
print(f"Số kết quả: {len(r8['sources'])}")

print("\nTất cả tools hoạt động!")