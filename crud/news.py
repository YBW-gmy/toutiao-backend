from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy import select,func,update,delete
from models.news import Category,News
from models.favorite import Favorite

async def get_all_news_for_indexing(db: AsyncSession) -> list[News]:
    """获取全部新闻用于向量索引构建"""
    stmt = select(News).order_by(News.id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
   stmt = select(News).where(News.category_id==category_id).offset(skip).limit(limit)
   result = await db.execute(stmt)
   return result.scalars().all()

async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(db:AsyncSession,news_id:int):
   stmt=update(News).where(News.id==news_id).values(views=News.views+1)
   result=await db.execute(stmt)
   await db.commit()
   return result.rowcount>0

async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
   stmt=select(News).where(News.category_id==category_id,News.id!=news_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
   result=await db.execute(stmt)
   related_news=result.scalars().all()
   #列表推导式
   return [{"id":news_detail.id,
           "title":news_detail.title,
           "content":news_detail.content,
           "image":news_detail.image,
           "author":news_detail.author,
           "publishTime":news_detail.publish_time,
           "categoryId":news_detail.category_id,
           "views":news_detail.views,}for news_detail in related_news]


