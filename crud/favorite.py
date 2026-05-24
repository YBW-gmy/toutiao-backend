from sqlalchemy import select, delete
from models.favorite import Favorite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from models.users import User
from models.news import News

#检验用户是不是收藏了新闻
async def is_new_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int,
):
    query=select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result=await db.execute(query)
    return result.scalar_one_or_none() is not None


async def add_news_favorite(
        db:AsyncSession,
        news_id:int,
        user_id:int
):
    favorite=Favorite(news_id=news_id,user_id=user_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite
#取消用户收藏
async def remove_news_favorite(db:AsyncSession, news_id:int, user_id:int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0
#查看新闻收藏
async def get_favorite_list(db:AsyncSession,
                            user_id:int,
                            page:int=1,
                            page_size:int=10):
    #总量+收藏的新闻列表
    count_query=select(func.count()).where(Favorite.user_id == user_id)
    count_result=await db.execute(count_query)
    total=count_result.scalar_one()
    #获取收藏的列表+连表查询具体的新闻信息
    offset=page_size*(page-1)
    query=(select(News,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id")
      .join(Favorite, News.id == Favorite.news_id)
      .where(Favorite.user_id == user_id)
      .order_by(Favorite.created_at.desc())
      .offset(offset).limit(page_size))
       )
    result=await db.execute(query)
    rows= result.all()
    return rows,total

async def clear_favorite(db:AsyncSession, user_id:int):
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0


