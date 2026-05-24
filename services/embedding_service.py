import os
import asyncio

# 国内优先使用 HuggingFace 镜像，避免下载失败
if "HF_ENDPOINT" not in os.environ:
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from sentence_transformers import SentenceTransformer
from config.rag_config import EMBEDDING_MODEL_NAME, MAX_EMBEDDING_TEXT_LENGTH

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


async def embed_single(text: str) -> list[float]:
    model = _get_model()
    truncated = text[:MAX_EMBEDDING_TEXT_LENGTH]
    vec = await asyncio.to_thread(
        model.encode, truncated, normalize_embeddings=True
    )
    return vec.tolist()


async def embed_batch(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    truncated = [t[:MAX_EMBEDDING_TEXT_LENGTH] for t in texts]
    vecs = await asyncio.to_thread(
        model.encode, truncated,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=False,
    )
    return vecs.tolist()
