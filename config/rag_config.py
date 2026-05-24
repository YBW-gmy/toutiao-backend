import os

# DeepSeek API
DEEPSEEK_URL = os.getenv("DEEPSEEK_URL", "https://api.deepseek.com/v1/chat/completions")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# Embedding Model
EMBEDDING_MODEL_NAME = "BAAI/bge-small-zh-v1.5"

# ChromaDB
CHROMA_PERSIST_DIR = "./chroma_db"
CHROMA_COLLECTION_NAME = "news_collection"

# Retrieval
RETRIEVAL_TOP_K = 5
MAX_EMBEDDING_TEXT_LENGTH = 512
MAX_CONTENT_LENGTH = 2000  # truncate full content in prompt to avoid exceeding context

# RAG Prompt Template
RAG_SYSTEM_PROMPT = (
    "你是一个专业的新闻问答助手。请严格根据以下检索到的新闻内容回答用户的问题。\n\n"
    "重要规则：\n"
    "1. 只能使用「检索到的相关新闻」中明确提及的信息，不得使用你训练数据中的知识\n"
    "2. 如果检索到的新闻不足以回答问题，直接告诉用户「抱歉，当前新闻库中没有足够的相关信息来回答这个问题」，不要编造任何信息\n"
    "3. 每个关键事实后面必须用方括号标注来源编号，例如[1]、[2]\n"
    "4. 如果引用具体数据（数字、日期、百分比），必须确保该数据来自检索到的新闻\n"
    "5. 回答中用到的每条新闻都必须至少引用一次\n\n"
    "检索到的相关新闻：\n"
    "{context}"
)
