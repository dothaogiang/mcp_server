# rag/hybrid_search.py
"""
Nhận câu hỏi từ chatbot
→ embed bằng bge-m3 (ra cả dense lẫn sparse)
→ tìm trong Qdrant bằng cả 2 loại vector
→ RRF gộp kết quả
→ trả về list các chunk liên quan kèm archive_id
"""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    SparseVector,
    Prefetch,
    FusionQuery,
    Fusion,
)
from rag.embedder import embed
from config import settings

client = QdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
    timeout=60,
)
COLLECTION = settings.qdrant_collection


def hybrid_search(query: str, top_k: int = 5) -> list[dict]:
    # 1. Embed câu hỏi → dense + sparse
    output = embed([query])
    dense_vec = output["dense_vecs"][0].tolist()
    sparse_weights = output["lexical_weights"][0]
    indices = [int(k) for k in sparse_weights.keys()]
    values = [float(v) for v in sparse_weights.values()]

    # 2. Tìm kiếm hybrid — Qdrant chạy dense và sparse song song
    #    rồi dùng RRF gộp lại theo rank
    results = client.query_points(
        collection_name=COLLECTION,
        prefetch=[
            # Dense: hiểu ngữ nghĩa
            Prefetch(query=dense_vec, using="dense", limit=top_k * 2),
            # Sparse: khớp tên riêng / mã số
            Prefetch(
                query=SparseVector(indices=indices, values=values),
                using="sparse",
                limit=top_k * 2,
            ),
        ],
        # RRF gộp 2 danh sách theo thứ hạng
        query=FusionQuery(fusion=Fusion.RRF),
        limit=top_k,
    )

    # 3. Trả về kết quả dạng dễ dùng
    return [
        {
            "archive_id": r.payload["archive_id"],
            "chunk": r.payload["chunk"],
            "chunk_index": r.payload["chunk_index"],
            "score": r.score,
        }
        for r in results.points
    ]
