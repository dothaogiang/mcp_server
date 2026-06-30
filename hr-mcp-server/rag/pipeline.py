# rag/pipeline.py
"""
Nhận document JSON từ Document API
→ cắt thành chunks nhỏ (500 token, overlap 100)
→ embed từng chunk bằng bge-m3
→ lưu vào Qdrant (dense + sparse)
"""
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance,
    SparseVectorParams, SparseVector,
    PointStruct,
)
from rag.embedder import embed
from config import settings

client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    timeout=60,
)
COLLECTION = settings.qdrant_collection


# ── 1. Tạo collection (chỉ chạy lần đầu) ──────────────────────────
def create_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION in existing:
        print(f"Collection '{COLLECTION}' đã tồn tại, bỏ qua.")
        return
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config={"dense": VectorParams(size=1024, distance=Distance.COSINE)},
        sparse_vectors_config={"sparse": SparseVectorParams()},
    )
    print(f"Tạo collection '{COLLECTION}' thành công!")


# ── 2. Cắt text thành chunks ───────────────────────────────────────
def chunk_text(text: str, size=500, overlap=100) -> list[str]:
    """
    Cắt theo từ (word-level)
    size    : số từ mỗi chunk
    overlap : số từ lặp lại giữa 2 chunk liên tiếp
              → giúp không mất ngữ cảnh ở ranh giới chunk
    """
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunks.append(" ".join(words[i: i + size]))
        i += size - overlap
    return chunks


# ── 3. Chuyển document JSON thành text phẳng ──────────────────────
def doc_to_text(doc: dict) -> str:
    """
    Document API trả về JSON nhiều field
    → nối tất cả value thành 1 chuỗi để embed
    """
    parts = []
    for key, value in doc.items():
        if isinstance(value, str) and value.strip():
            parts.append(f"{key}: {value}")
        elif isinstance(value, dict):
            for k2, v2 in value.items():
                if isinstance(v2, str) and v2.strip():
                    parts.append(f"{k2}: {v2}")
    return "\n".join(parts)


# ── 4. Index 1 document vào Qdrant ────────────────────────────────
def index_document(archive_id: str, doc: dict):
    text = doc_to_text(doc)
    chunks = chunk_text(text)

    if not chunks:
        print(f"  Bỏ qua {archive_id} — không có text")
        return

    # Xoá các chunk cũ của archive này trước khi index lại
    # (tránh chunk cũ "rác" còn sót khi nội dung archive đã thay đổi)
    delete_document(archive_id)

    outputs = embed(chunks)
    points = []

    for i, chunk in enumerate(chunks):
        dense_vec = outputs["dense_vecs"][i].tolist()
        sparse_weights = outputs["lexical_weights"][i]
        indices = [int(k) for k in sparse_weights.keys()]
        values = [float(v) for v in sparse_weights.values()]

        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector={
                "dense": dense_vec,
                "sparse": SparseVector(indices=indices, values=values),
            },
            payload={
                "archive_id": archive_id,
                "chunk": chunk,
                "chunk_index": i,
            }
        ))

    client.upsert(collection_name=COLLECTION, points=points)
    print(f"  ✓ Indexed {len(points)} chunks — archive {archive_id}")


# ── 5. Xoá toàn bộ chunk của 1 archive ─────────────────────────────
def delete_document(archive_id: str):
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client.delete(
        collection_name=COLLECTION,
        points_selector=Filter(
            must=[FieldCondition(key="archive_id", match=MatchValue(value=archive_id))]
        ),
    )
