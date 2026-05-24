from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from crud import favorite
from schemas.favorite import FavoriteListResponse
from schemas.favorite import FavoriteCheckResponse
from schemas.favorite import FavoriteAddRequest
from fastapi import HTTPException

router = APIRouter(prefix='/api/favorite',tags=['favorite'])
#查看新闻收藏
@router.get('/check')
async def check_favorite(news_id:int=Query(...,alias='newsId'),user:User=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):
    is_favorite = await favorite.is_new_favorite(db,user.id,news_id)

    return success_response(message='检查收藏状态成功',data=FavoriteCheckResponse(isFavorite=is_favorite))
#添加新闻收藏
@router.post('/add')
async def add_favorite(data:FavoriteAddRequest,user:User=Depends(get_current_user),
                       db:AsyncSession=Depends(get_db)):
    result=await favorite.add_news_favorite(db,data.news_id,user.id)
    return success_response(message='添加收藏成功',data=result)

#删除新闻收藏
@router.delete('/remove')
async def remove_favorite(news_id:int=Query(...,alias='newsId'),user:User=Depends(get_current_user),
                          db:AsyncSession=Depends(get_db)):
    result=await favorite.remove_news_favorite(db,news_id,user.id)
    if not result:
        raise HTTPException(status_code=404,detail='收藏记录不存在')
    return success_response(message='删除收藏成功')
#获取用户收藏列表
@router.get('/list')
async def get_favorite_list(user:User=Depends(get_current_user),
                            db:AsyncSession=Depends(get_db),
                            page:int=Query(default=1,ge=1),
                            page_size:int=Query(default=10,ge=1,le=100,alias='pageSize')):
    rows,total=await favorite.get_favorite_list(db,user.id,page,page_size)
    favorite_list=[
        {
            **news.__dict__,
            "favorite_time":favorite_time,
            "favorite_id":favorite_id
        } for news,favorite_time,favorite_id in rows
    ]
    has_more=(page*page_size)<total
    data=FavoriteListResponse(list=favorite_list,total=total,hasMore=has_more)

    return success_response(message='获取收藏列表成功',data=data)
# 删除用户收藏
@router.delete('/clear')
async def clear_favorite(user:User=Depends(get_current_user),
                         db:AsyncSession=Depends(get_db)):
      count=await favorite.clear_favorite(db,user.id)
      return success_response(message=f'清空了{count}条收藏记录')