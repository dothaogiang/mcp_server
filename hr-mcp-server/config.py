# config.py
"""Application configuration — nguồn cấu hình duy nhất cho toàn bộ project.

Mọi module (rag, db, sync, tools, main) đều phải import settings từ đây
thay vì tự đọc os.getenv() rải rác, để tránh lệch giá trị mặc định
giữa các nơi.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Postgres
    postgres_url: str = "postgresql://postgres:postgres@localhost:5432/hr_archive"

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "hr_documents"

    # Backend APIs
    search_api_url: str = "http://localhost:8001/api/public/archives"
    document_api_url: str = "http://localhost:8001/api/public/archives"
    staff_profile_api_url: str = "http://localhost:8001/api/public/staff-profiles"
    file_api_url: str = "http://localhost:8001/api/public/files/proxy"

    # Webhook auth — backend phải gửi header X-Webhook-Secret đúng giá trị này
    webhook_secret: str = "change-me"

    # MCP server auth — chatbot/client phải gửi header Authorization: Bearer <mcp_api_key>
    mcp_api_key: str = "change-me"


settings = Settings()
