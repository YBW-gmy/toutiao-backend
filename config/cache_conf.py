import redis.asyncio as redis
import json
from typing import Any



REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


# 创建Redis连接
redis_client =redis.Redis(
    host=REDIS_HOST,#Redis服务地址
    port=REDIS_PORT,#Redis端口
    db=REDIS_DB,#Redis数据库编号
    decode_responses=True#将字节数据编码为字符串
)

#设置和读取字符串 ，列表和字典
#读取字符串
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取Redis缓存数据失败: {e}")
        return None
#读取字典或者列表
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取JSON缓存数据失败: {e}")
        return None

#存缓存
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,dict) or isinstance(value,list):
            value = json.dumps(value,ensure_ascii=False)
        return await redis_client.set(key, value, expire)
    except Exception as e:
        print(f"设置Redis缓存数据失败: {e}")
        return None