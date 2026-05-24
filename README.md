# 新闻聚合平台后端 + RAG本地知识库问答
基于 FastAPI 开发的新闻资讯后端系统，集成 RAG 实现 AI 智能问答，支持异步高并发、流式响应与向量检索。

## 技术栈
Python / FastAPI / SQLAlchemy(异步) / MySQL / Redis / DeepSeek API / LangChain / RAG / Docker

## 功能亮点
- 用户认证：自定义Token + bcrypt+SHA‑256密码哈希，实现注册登录
- 缓存架构：MySQL+Redis双层缓存，降低数据库压力
- RAG问答：完整实现文本嵌入→向量检索→Top‑K召回→LLM流式生成→原文溯源
- 工程规范：统一响应格式、Pydantic参数校验、全局异常拦截
