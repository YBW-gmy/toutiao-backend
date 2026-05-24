from pydantic import BaseModel, Field


class RAGChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="用户问题")


class SyncResponse(BaseModel):
    indexed_count: int = Field(..., description="已索引的新闻总数")
    message: str = Field(default="同步成功", description="状态信息")
