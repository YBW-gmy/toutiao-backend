from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import history
from schemas.history import HistoryListResponse, HistoryAddRequest
from utils.exception_handlers import HTTPException

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await history.add_browse_history(db, user.id, data.news_id)
    return success_response(message="添加浏览历史成功", data=result)


@router.delete("/remove")
async def remove_history(
    history_id: int = Query(..., alias="historyId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await history.delete_history_entry(db, user.id, history_id)
    if not result:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    return success_response(message="删除浏览历史成功")


@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    count = await history.clear_history(db, user.id)
    return success_response(message=f"清空了{count}条浏览历史记录")


@router.get("/list")
async def get_history_list(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100, alias="pageSize"),
):
    rows, total = await history.get_history_list(db, user.id, page, page_size)
    history_list = [
        {
            **news.__dict__,
            "view_time": view_time,
            "history_id": history_id,
        }
        for news, view_time, history_id in rows
    ]
    has_more = (page * page_size) < total
    data = HistoryListResponse(list=history_list, total=total, hasMore=has_more)
    return success_response(message="获取浏览历史列表成功", data=data)
