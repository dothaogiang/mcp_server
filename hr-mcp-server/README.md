# HR OCR MCP Server

MCP server expose các tool tra cứu hồ sơ lưu trữ nhân sự (search, chi tiết hồ sơ,
hồ sơ cán bộ, file, RAG semantic search) cho chatbot gọi qua giao thức MCP
(Streamable HTTP).

## Kiến trúc

- `tools/` — MCP tool, gọi sang Backend API (search/document/staff/file).
- `rag/` — embed bằng bge-m3 (dense + sparse) + hybrid search trên Qdrant.
- `db/` — lưu bản sao archive vào Postgres (đọc nhanh, không phụ thuộc Backend).
- `sync/` — đồng bộ dữ liệu: `scheduler.py` (mỗi giờ) hoặc `webhook.py` (real-time,
  có xác thực bằng `WEBHOOK_SECRET`). Mỗi lần sync archive sẽ đồng thời ghi
  Postgres và index vào Qdrant.
- `main.py` — chạy MCP server (port 8000), có xác thực `MCP_API_KEY`.

## Cài đặt

```bash
cp .env.example .env   # rồi điền giá trị thật
pip install -r requirements.txt
python db/init_db.py            # tạo bảng Postgres
python main.py                  # chạy MCP server :8000
```

Hoặc chạy toàn bộ bằng Docker:

```bash
docker compose up --build
```

## Chạy đồng bộ dữ liệu

```bash
python sync/fetch_archives.py   # sync 1 lần, ngay lập tức
python sync/scheduler.py        # sync ngay + lặp lại mỗi 1 tiếng
python run_webhook.py           # nhận webhook real-time từ Backend, port 8002
```

## Bảo mật — đọc trước khi deploy

- File `.env` từng bị commit vào git ở phiên bản trước — **đã đổi mật khẩu
  Postgres và xoá `.env` khỏi lịch sử git là việc bắt buộc phải làm** trước khi
  public repo này thêm bất kỳ commit nào nữa.
- MCP server yêu cầu header `Authorization: Bearer <MCP_API_KEY>`.
- Webhook yêu cầu header `X-Webhook-Secret: <WEBHOOK_SECRET>`.
