from fastapi import Header,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from crud import users
from schemas.users import UserInfoResponse
from fastapi import HTTPException


#用户认证
#整合 根据Token获取用户信息，返回用户
async def get_current_user(authorization: str=Header(default="...",alias="Authorization"),
db: AsyncSession = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user= await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=401,detail="无效令牌或者过期")
    return user


async def get_optional_user(
    authorization: str = Header(default="", alias="Authorization"),
    db: AsyncSession = Depends(get_db),
):
    if not authorization:
        return None
    token = authorization.replace("Bearer ", "")
    user = await users.get_user_by_token(db, token)
    return user