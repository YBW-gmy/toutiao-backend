from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from datetime import datetime
from typing import List
from schemas.base import NewsItemBase

class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias='isFavorite')
    model_config = ConfigDict(populate_by_name=True)

class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId')
    model_config = ConfigDict(populate_by_name=True)

class FavoriteNewItemReponse(NewsItemBase):
    favorite_time: datetime = Field(..., alias='favoriteTime')
    favorite_id: int = Field(..., alias='favoriteId')
    model_config = ConfigDict(populate_by_name=True,
                              from_attributes=True)
class FavoriteListResponse(BaseModel):
    list: List[FavoriteNewItemReponse] = Field(..., alias='list')
    total: int = Field(..., alias='total')
    has_more: bool = Field(..., alias='hasMore')
    model_config = ConfigDict(populate_by_name=True,
                              attributes=True)