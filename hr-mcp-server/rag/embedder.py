# rag/embedder.py
# Load model 1 lần duy nhất khi import — tránh load lại mỗi lần gọi
_model = None


def get_model():
    global _model
    if _model is None:
        try:
            from FlagEmbedding import BGEM3FlagModel
        except Exception as exc:
            raise RuntimeError(
                "RAG dependencies are not available. Please install FlagEmbedding and a compatible PyTorch runtime."
            ) from exc

        print("Đang load model bge-m3")
        _model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
        print("Load model xong!")
    return _model

def embed(texts: list[str]) -> dict:
    """
    Nhận vào list các đoạn text
    Trả về dict gồm:
      - dense_vecs : list vector số thực (hiểu ngữ nghĩa)
      - lexical_weights: list dict token→weight (khớp từ khoá)
    """
    model = get_model()
    output = model.encode(
        texts,
        return_dense=True,
        return_sparse=True,
    )
    return {
        "dense_vecs": output["dense_vecs"],
        "lexical_weights": output["lexical_weights"],
    }