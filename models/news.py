
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import DateTime, String, Integer, Index, Text, ForeignKey
from typing import Optional

from models import Base
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer,comment="排序",default=0,nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="更新时间"
    )
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}',sort_order={self.sort_order})>"

class News(Base):
        """新闻表模型类，用于存储新闻的基础信息"""
        __tablename__ = "news"

        # 定义表级索引，提升查询性能
        __table_args__ = (
            # 为分类ID创建索引，提升按分类查询新闻的速度
            Index("fk_news_category_idx", "category_id"),
            # 为发布时间创建索引，提升按时间排序/筛选新闻的速度
            Index("idx_publish_time", "publish_time"),
        )

        # 新闻ID：主键，自增
        id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            autoincrement=True,
            comment="新闻ID"
        )

        # 新闻标题：非空，最大长度255字符
        title: Mapped[str] = mapped_column(
            String(255),
            nullable=False,
            comment="新闻标题"
        )

        # 新闻简介：可选，最大长度500字符
        description: Mapped[Optional[str]] = mapped_column(
            String(500),
            comment="新闻简介"
        )

        # 新闻内容：非空，Text类型支持长文本
        content: Mapped[str] = mapped_column(
            Text,
            nullable=False,
            comment="新闻内容"
        )

        # 封面图片URL：可选，最大长度255字符
        image: Mapped[Optional[str]] = mapped_column(
            String(255),
            comment="封面图片URL"
        )

        # 作者：可选，最大长度50字符
        author: Mapped[Optional[str]] = mapped_column(
            String(50),
            comment="作者"
        )

        # 分类ID：外键关联news_category表的id，非空
        category_id: Mapped[int] = mapped_column(
            Integer,
            ForeignKey("news_category.id"),
            nullable=False,
            comment="分类ID"
        )

        # 浏览量：默认值为0，非空
        views: Mapped[int] = mapped_column(
            Integer,
            default=0,
            nullable=False,
            comment="浏览量"
        )

        # 发布时间：默认值为当前时间，非空
        publish_time: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.now,
            comment="发布时间"
        )
        created_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.now,
            comment="创建时间"
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime,
            default=datetime.now,
            comment="更新时间"
        )