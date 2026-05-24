from datetime import datetime

from sqlalchemy import Index, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Favorite(Base):
    __tablename__ = "favorite"

    __table_args__ = (
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
        Index("uq_user_news", "user_id", "news_id", unique=True),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="收藏ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("news.id"), nullable=False, comment="新闻ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="收藏时间"
    )

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
