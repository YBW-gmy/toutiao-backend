from sqlalchemy import select, delete
from models.history import BrowseHistory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from models.news import News


async def add_browse_history(db: AsyncSession, user_id: int, news_id: int):
    record = BrowseHistory(user_id=user_id, news_id=news_id)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def delete_history_entry(db: AsyncSession, user_id: int, history_id: int):
    stmt = delete(BrowseHistory).where(
        BrowseHistory.user_id == user_id, BrowseHistory.id == history_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int):
    stmt = delete(BrowseHistory).where(BrowseHistory.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0


async def get_history_list(
    db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10
):
    count_query = select(func.count()).where(BrowseHistory.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = page_size * (page - 1)
    query = (
        select(
            News,
            BrowseHistory.view_time.label("view_time"),
            BrowseHistory.id.label("history_id"),
        )
        .join(BrowseHistory, News.id == BrowseHistory.news_id)
        .where(BrowseHistory.user_id == user_id)
        .order_by(BrowseHistory.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return rows, total
