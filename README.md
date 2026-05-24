# 新闻资讯后端 + RAG 智能问答

基于 FastAPI 的新闻头条后端系统，集成 RAG（检索增强生成）实现 AI 智能问答。

## 技术栈

- **后端框架**: FastAPI + SQLAlchemy 2.0 异步 ORM
- **数据库**: MySQL 8.x + Redis 7.x
- **RAG 管道**: BAAI/bge-small-zh-v1.5 → ChromaDB → DeepSeek → SSE 流式输出
- **AI 模型**: DeepSeek Chat API / BGE 中文嵌入模型

## 功能模块

| 模块 | 说明 |
|------|------|
| 新闻管理 | 分类浏览、详情查看、相关推荐、浏览量统计 |
| 用户系统 | 注册登录、Token 鉴权、个人信息管理 |
| 收藏/历史 | 新闻收藏、浏览历史记录 |
| AI 问答 | RAG 检索增强生成，流式回答 + 原文溯源引用 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 为 .env 并填入真实值）
cp .env.example .env

# 同步新闻到向量库
curl -X POST http://127.0.0.1:8000/api/chat/rag/sync

# 启动服务
uvicorn main:app --host 127.0.0.1 --port 8000
```

## 项目结构

```
├── main.py              # 应用入口
├── config/              # 数据库 / RAG / 缓存配置
├── models/              # SQLAlchemy ORM 模型
├── schemas/             # Pydantic 请求响应模型
├── routers/             # API 路由
├── crud/                # 数据库操作层
├── services/            # RAG 服务（嵌入 / 向量库 / 生成）
├── cache/               # Redis 缓存
└── utils/               # 认证 / 安全 / 异常处理
```

## RAG 流程

```
用户提问 → BGE 嵌入 → ChromaDB 余弦检索 Top-5 → MySQL 取全文 → DeepSeek 流式生成 → SSE + 来源标注
```
