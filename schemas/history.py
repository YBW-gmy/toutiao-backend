from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from datetime import datetime
from typing import List
from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")
    model_config = ConfigDict(populate_by_name=True)


class HistoryItemResponse(NewsItemBase):
    view_time: datetime = Field(..., alias="viewTime")
    history_id: int = Field(..., alias="historyId")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class HistoryListResponse(BaseModel):
    list: List[HistoryItemResponse] = Field(..., alias="list")
    total: int = Field(..., alias="total")
    has_more: bool = Field(..., alias="hasMore")
    model_config = ConfigDict(populate_by_name=True)
