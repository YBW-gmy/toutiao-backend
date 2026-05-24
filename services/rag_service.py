import json
import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from config.rag_config import (
    DEEPSEEK_URL,
    DEEPSEEK_KEY,
    DEEPSEEK_MODEL,
    RAG_SYSTEM_PROMPT,
    RETRIEVAL_TOP_K,
    MAX_CONTENT_LENGTH,
)
from services.embedding_service import embed_single
from services.vector_store import search_similar


async def stream_rag_answer(query: str, db: AsyncSession):
    """RAG 问答流式生成器：嵌入查询 → 检索 → 构建 prompt → DeepSeek 流式生成 → 返回来源"""
    # Step 1: embed query
    query_vec = await embed_single(query)

    # Step 2: search similar news
    raw_results = await search_similar(query_vec, top_k=RETRIEVAL_TOP_K)

    # Step 3: extract sources from ChromaDB results
    sources = _extract_sources(raw_results)

    # Step 4: fetch full content from DB for each retrieved news
    from crud.news import get_news_detail

    retrieved_news = []
    for src in sources:
        detail = await get_news_detail(db, src["id"])
        if detail:
            retrieved_news.append(detail)

    # Step 5: build context string
    context_parts = []
    for i, news in enumerate(retrieved_news, 1):
        content = (news.content or "")[:MAX_CONTENT_LENGTH]
        context_parts.append(
            f"[{i}] 标题：{news.title}\n"
            f"描述：{news.description or ''}\n"
            f"内容：{content}\n"
            f"发布时间：{news.publish_time}\n"
        )
    context_text = "\n".join(context_parts) if context_parts else "暂无相关新闻。"
    system_prompt = RAG_SYSTEM_PROMPT.format(context=context_text)

    # Step 6: stream from DeepSeek
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    async with httpx.AsyncClient(timeout=httpx.Timeout(60)) as client:
        async with client.stream(
            "POST",
            DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "stream": True,
            },
        ) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

    # Step 7: yield sources event after stream completes
    sources_json = json.dumps(
        {"type": "sources", "data": sources},
        ensure_ascii=False,
    )
    yield f"data: {sources_json}\n\n".encode("utf-8")


async def stream_chat_with_rag(messages: list[dict], db: AsyncSession):
    """对前端 /api/chat 的消息格式做 RAG 增强：取最后一条 user 消息做检索，注入 System Prompt"""
    # 取最后一条用户消息作为检索查询
    user_query = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_query = m["content"]
            break

    if not user_query:
        # 无用户消息，直接透传
        async with httpx.AsyncClient(timeout=httpx.Timeout(60)) as client:
            async with client.stream(
                "POST", DEEPSEEK_URL,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {DEEPSEEK_KEY}",
                },
                json={"model": DEEPSEEK_MODEL, "messages": messages, "stream": True},
            ) as response:
                async for chunk in response.aiter_bytes():
                    yield chunk
        return

    # 检索 + 构建上下文
    query_vec = await embed_single(user_query)
    raw_results = await search_similar(query_vec, top_k=RETRIEVAL_TOP_K)
    sources = _extract_sources(raw_results)

    from crud.news import get_news_detail

    retrieved_news = []
    for src in sources:
        detail = await get_news_detail(db, src["id"])
        if detail:
            retrieved_news.append(detail)

    context_parts = []
    for i, news in enumerate(retrieved_news, 1):
        content = (news.content or "")[:MAX_CONTENT_LENGTH]
        context_parts.append(
            f"[{i}] 标题：{news.title}\n"
            f"描述：{news.description or ''}\n"
            f"内容：{content}\n"
            f"发布时间：{news.publish_time}\n"
        )
    context_text = "\n".join(context_parts) if context_parts else "暂无相关新闻。"

    system_prompt = RAG_SYSTEM_PROMPT.format(context=context_text)

    # 在 messages 最前面插入 RAG system prompt
    rag_messages = [{"role": "system", "content": system_prompt}] + messages

    async with httpx.AsyncClient(timeout=httpx.Timeout(60)) as client:
        async with client.stream(
            "POST", DEEPSEEK_URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_KEY}",
            },
            json={"model": DEEPSEEK_MODEL, "messages": rag_messages, "stream": True},
        ) as response:
            async for chunk in response.aiter_bytes():
                yield chunk

    # 末尾追加 sources
    sources_json = json.dumps(
        {"type": "sources", "data": sources},
        ensure_ascii=False,
    )
    yield f"data: {sources_json}\n\n".encode("utf-8")


def _extract_sources(raw_results) -> list[dict]:
    """将 ChromaDB 查询结果转为简洁的来源列表"""
    sources = []
    ids_list = raw_results.get("ids", [[]])[0]
    metadatas_list = raw_results.get("metadatas", [[]])[0]
    distances_list = raw_results.get("distances", [[]])[0]

    for doc_id, meta, dist in zip(ids_list, metadatas_list, distances_list):
        sources.append({
            "id": int(doc_id),
            "title": meta.get("title", ""),
            "description": meta.get("description", ""),
            "publishTime": meta.get("publish_time", ""),
            "score": round(1.0 - dist, 4) if dist else 0.0,
        })
    return sources
