from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict
from typing import Optional

class NewsItemBase(BaseModel):
    id: int = Field(..., alias='id')
    title: str = Field(..., alias='title')
    description: str = Field(..., alias='description')
    image: str = Field(..., alias='image')
    author: str = Field(..., alias='author')
    category_id: int = Field(..., alias='categoryId')
    views: int = Field(..., alias='views')
    publish_time: datetime = Field(..., alias='publishTime')
    model_config = ConfigDict(populate_by_name=True,
                              from_attributes=True)