from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy import select,func,update,delete
from models.news import Category,News
from cache.news_cache import get_cached_categories,set_cached_categories,get_cached_news_list,set_cached_news_list,get_cached_news_count,set_cached_news_count,get_cached_news_detail,set_cached_news_detail,get_cached_related_news,set_cached_related_news
from fastapi.encoders import jsonable_encoder
async def get_categories(db: AsyncSession,skip: int = 0, limit: int = 100):
    #先尝试从缓存中读取数据
    cached_categories=await get_cached_categories()
    if cached_categories:
        return cached_categories
    #如果没有数据，则从数据库中读取数据
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories=result.scalars().all()
    #缓存中没有数据，则从数据库中读取数据
    if categories:
        #写入缓存
        categories=jsonable_encoder(categories)
        await set_cached_categories(categories)
    #返回数据
    return categories

async def get_news_list(db:AsyncSession,category_id:int,skip:int=0,limit:int=10):
    #先尝试从缓存中读取新闻列表
    cached_news_list=await get_cached_news_list(category_id,skip,limit)
    if cached_news_list:
        return cached_news_list
    #缓存中没有数据，则从数据库中读取
    stmt = select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list=result.scalars().all()
    if news_list:
        #写入缓存
        news_list=jsonable_encoder(news_list)
        await set_cached_news_list(category_id,skip,limit,news_list)
    return news_list

async def get_news_count(db:AsyncSession,category_id:int):
    #先尝试从缓存中读取新闻总数
    cached_count=await get_cached_news_count(category_id)
    if cached_count is not None:
        return cached_count
    #缓存中没有数据，则从数据库中读取
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    total=result.scalar_one()
    #写入缓存
    await set_cached_news_count(category_id,total)
    return total

async def get_news_detail(db:AsyncSession,news_id:int):
    #先尝试从缓存中读取新闻详情
    cached_detail=await get_cached_news_detail(news_id)
    if cached_detail:
        return cached_detail
    #缓存中没有数据，则从数据库中读取
    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    news_detail=result.scalar_one_or_none()
    if news_detail:
        #写入缓存
        news_detail=jsonable_encoder(news_detail)
        await set_cached_news_detail(news_id,news_detail)
    return news_detail

async def increase_news_views(db:AsyncSession,news_id:int):
   stmt=update(News).where(News.id==news_id).values(views=News.views+1)
   result=await db.execute(stmt)
   await db.commit()
   return result.rowcount>0

async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int=5):
   #先尝试从缓存中读取相关新闻
   cached_related=await get_cached_related_news(news_id,category_id)
   if cached_related:
       return cached_related
   #缓存中没有数据，则从数据库中读取
   stmt=select(News).where(News.category_id==category_id,News.id!=news_id).order_by(News.views.desc(),News.publish_time.desc()).limit(limit)
   result=await db.execute(stmt)
   related_news=result.scalars().all()
   if related_news:
       #列表推导式
       related_list=[{"id":news_detail.id,
               "title":news_detail.title,
               "content":news_detail.content,
               "image":news_detail.image,
               "author":news_detail.author,
               "publishTime":news_detail.publish_time,
               "categoryId":news_detail.category_id,
               "views":news_detail.views,}for news_detail in related_news]
       #写入缓存
       await set_cached_related_news(news_id,category_id,related_list)
       return related_list
   return []
