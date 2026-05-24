from config.cache_conf import get_json_cache,set_cache
from typing import List,Dict,Any
#新闻相关的缓存方法
#key-value

CATEGORY_E_KEY = "news:category"
NEWS_LIST_KEY = "news:list:{}:{}:{}"
NEWS_COUNT_KEY = "news:count:{}"
NEWS_DETAIL_KEY = "news:detail:{}"
NEWS_RELATED_KEY = "news:related:{}:{}"

#获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORY_E_KEY)

#写入新闻分类缓存:缓存数据，过期时间
#分类配置，数据越稳定，缓存时间越长
async def set_cached_categories(data:List[Dict[str, Any]],expire:int=7200):
    return await set_cache(CATEGORY_E_KEY,data,expire=expire)

#获取新闻列表缓存
async def get_cached_news_list(category_id:int,skip:int,limit:int):
    key = NEWS_LIST_KEY.format(category_id,skip,limit)
    return await get_json_cache(key)

#写入新闻列表缓存
async def set_cached_news_list(category_id:int,skip:int,limit:int,data:List[Dict[str, Any]],expire:int=600):
    key = NEWS_LIST_KEY.format(category_id,skip,limit)
    return await set_cache(key,data,expire=expire)

#获取新闻总数缓存
async def get_cached_news_count(category_id:int):
    key = NEWS_COUNT_KEY.format(category_id)
    return await get_json_cache(key)

#写入新闻总数缓存
async def set_cached_news_count(category_id:int,total:int,expire:int=600):
    key = NEWS_COUNT_KEY.format(category_id)
    return await set_cache(key,total,expire=expire)

#获取新闻详情缓存
async def get_cached_news_detail(news_id:int):
    key = NEWS_DETAIL_KEY.format(news_id)
    return await get_json_cache(key)

#写入新闻详情缓存
async def set_cached_news_detail(news_id:int,data:Dict[str, Any],expire:int=300):
    key = NEWS_DETAIL_KEY.format(news_id)
    return await set_cache(key,data,expire=expire)

#获取相关新闻缓存
async def get_cached_related_news(news_id:int,category_id:int):
    key = NEWS_RELATED_KEY.format(category_id,news_id)
    return await get_json_cache(key)

#写入相关新闻缓存
async def set_cached_related_news(news_id:int,category_id:int,data:List[Dict[str, Any]],expire:int=1200):
    key = NEWS_RELATED_KEY.format(category_id,news_id)
    return await set_cache(key,data,expire=expire)
