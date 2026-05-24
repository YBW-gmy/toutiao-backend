import httpx
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from config.rag_config import DEEPSEEK_URL, DEEPSEEK_KEY, DEEPSEEK_MODEL
from schemas.rag import RAGChatRequest
from services.rag_service import stream_rag_answer, stream_chat_with_rag
from services.vector_store import sync_from_db
from utils.response import success_response

router = APIRouter(prefix="/api/chat", tags=["ai_chat"])


class ChatRequest(BaseModel):
    messages: list[dict]


@router.post("")
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """AI 对话（含 RAG 新闻检索增强）"""
    return StreamingResponse(
        stream_chat_with_rag(request.messages, db),
        media_type="text/event-stream",
    )


@router.post("/rag")
async def chat_rag(
    request: RAGChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """RAG 智能新闻问答 —— 流式返回 DeepSeek 回答及引用来源"""
    return StreamingResponse(
        stream_rag_answer(request.query, db),
        media_type="text/event-stream",
    )


@router.post("/rag/sync")
async def sync_rag_index(
    db: AsyncSession = Depends(get_db),
):
    """管理端点：同步全部新闻到向量索引"""
    count = await sync_from_db(db)
    return success_response("向量索引同步成功", {"indexed_count": count})


@router.post("/rag")
async def chat_rag(
    request: RAGChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """RAG 智能新闻问答 —— 流式返回 DeepSeek 回答及引用来源"""
    return StreamingResponse(
        stream_rag_answer(request.query, db),
        media_type="text/event-stream",
    )


@router.post("/rag/sync")
async def sync_rag_index(
    db: AsyncSession = Depends(get_db),
):
    """管理端点：同步全部新闻到向量索引"""
    count = await sync_from_db(db)
    return success_response("向量索引同步成功", {"indexed_count": count})
