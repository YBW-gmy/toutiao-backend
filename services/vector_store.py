import asyncio
import chromadb
from chromadb.config import Settings
from sqlalchemy.ext.asyncio import AsyncSession

from config.rag_config import (
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
    RETRIEVAL_TOP_K,
)
from crud.news import get_all_news_for_indexing
from services.embedding_service import embed_batch, embed_single

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
    if _collection is None:
        _collection = _client.get_or_create_collection(
            name=CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


async def add_news_batch(
    ids: list[str],
    texts: list[str],
    metadatas: list[dict],
    embeddings: list[list[float]],
):
    coll = _get_collection()
    await asyncio.to_thread(
        coll.upsert,
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )


async def search_similar(query_embedding: list[float], top_k: int = RETRIEVAL_TOP_K):
    coll = _get_collection()
    results = await asyncio.to_thread(
        coll.query,
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return results


async def get_collection_count() -> int:
    coll = _get_collection()
    return await asyncio.to_thread(coll.count)


async def add_single_news(news_id: int, title: str, description: str, publish_time: str):
    """增量添加单条新闻到向量库"""
    text = f"{title} {description or ''}"
    vec = await embed_single(text)
    coll = _get_collection()
    await asyncio.to_thread(
        coll.upsert,
        ids=[str(news_id)],
        documents=[text],
        metadatas=[{
            "news_id": news_id,
            "title": title,
            "description": description or "",
            "publish_time": publish_time,
        }],
        embeddings=[vec],
    )


async def sync_from_db(db: AsyncSession) -> int:
    """从数据库读取所有新闻并同步到向量索引"""
    news_list = await get_all_news_for_indexing(db)

    if not news_list:
        return 0

    ids = []
    texts = []
    metadatas = []
    text_batch = []

    for row in news_list:
        nid = str(row.id)
        text = f"{row.title} {row.description or ''}"
        ids.append(nid)
        texts.append(text)
        text_batch.append(text)
        metadatas.append({
            "news_id": row.id,
            "title": row.title,
            "description": row.description or "",
            "publish_time": str(row.publish_time),
        })

    embeddings = await embed_batch(text_batch)
    coll = _get_collection()
    await asyncio.to_thread(
        coll.upsert,
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(news_list)
