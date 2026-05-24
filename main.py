from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from utils.exception_handlers import register_exception_handlers
from routers import news, users, favorite, history, ai_chat
from fastapi.middleware.cors import CORSMiddleware
import os


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """启动时自动同步新闻到 RAG 向量索引（取消注释以启用）"""
#     from config.db_config import AsyncSessionLocal
#     from services.vector_store import sync_from_db
#     async with AsyncSessionLocal() as db:
#         count = await sync_from_db(db)
#         print(f"RAG index synced: {count} articles")
#     yield

app = FastAPI()  # 如需自动同步，改为 FastAPI(lifespan=lifespan)
register_exception_handlers(app)  # 异常处理器
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# API路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)
app.include_router(ai_chat.router)

# 托管前端静态文件
FRONTEND_DIR = "D:/code/xwzx-news/dist"
assets_dir = os.path.join(FRONTEND_DIR, "assets")

if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found"}


