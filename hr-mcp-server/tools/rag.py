# tools/rag.py
from rag.hybrid_search import hybrid_search


def rag_query(query: str, top_k: int = 5) -> dict:
    results = hybrid_search(query, top_k)

    if not results:
        return {"context": "", "sources": []}

    context = "\n\n---\n\n".join([
        f"[Archive: {r['archive_id']}]\n{r['chunk']}"
        for r in results
    ])

    return {
        "context": context,
        "sources": [
            {
                "archive_id": r["archive_id"],
                "chunk_index": r["chunk_index"],
                "score": r["score"],
            }
            for r in results
        ]
    }