# sync/webhook.py
import hmac

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Union

from config import settings
from db.archive_store import upsert_archive
from rag.pipeline import index_document

app = FastAPI(title="Webhook Receiver")


class StaffMetadata(BaseModel):
    ho_va_ten: Optional[str] = None
    ngay_sinh: Optional[str] = None
    don_vi_cong_tac: Optional[str] = None
    dia_chi: Optional[str] = None
    chuc_vu: Optional[str] = None


class ArchivePayload(BaseModel):
    id: str
    title: Optional[str] = None
    arc_file_code: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    maintenance: Optional[str] = None
    staff_metadata: Optional[StaffMetadata] = None


def _verify_secret(x_webhook_secret: Optional[str]):
    """So sánh secret bằng hmac.compare_digest để tránh timing attack."""
    if not x_webhook_secret or not hmac.compare_digest(x_webhook_secret, settings.webhook_secret):
        raise HTTPException(status_code=401, detail="Webhook secret không hợp lệ")


@app.post("/webhook/archives")
async def receive_archive(
    payload: Union[ArchivePayload, list[ArchivePayload]],
    x_webhook_secret: Optional[str] = Header(None),
):
    _verify_secret(x_webhook_secret)

    archives = payload if isinstance(payload, list) else [payload]

    synced = []
    for archive in archives:
        data = archive.model_dump()
        upsert_archive(data)
        try:
            index_document(archive.id, data)
        except Exception as e:
            # Lỗi index RAG không nên làm fail toàn bộ webhook —
            # dữ liệu Postgres vẫn đã được lưu đúng.
            print(f"  ✗ Lỗi index RAG cho {archive.id}: {e}")
        synced.append(archive.id)

    return {"synced": len(synced), "ids": synced}
