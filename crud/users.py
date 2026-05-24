#根据用户名查询数据库
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy import select
from models.users import User
from schemas.users import UserRequest
from utils import security
import uuid
from sqlalchemy import update
from datetime import datetime,timedelta
from models.users import UserToken
from utils.exception_handlers import HTTPException
from schemas.users import UserUpdateRequest


async def get_user_by_username(db: AsyncSession, username: str):
     query = select(User).where(User.username == username)
     result = await db.execute(query)
     return result.scalar_one_or_none()

#创建用户
async  def create_user(db: AsyncSession, user_date:UserRequest):
# 密码加密
   hashed_password = security.get_hash_password(user_date.password)
   user = User(username=user_date.username,password=hashed_password)
   db.add(user)
   await db.commit()
   await db.refresh(user)#读取最新的user
   return user

#生成Token
async def create_token(db: AsyncSession, user_id:int):
    token=str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
        await db.commit()
        await db.refresh(user_token)
        return user_token
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
        await db.refresh(user_token)
        return user_token

async def authenticate_user(db: AsyncSession, username: str, password: str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    ok, need_upgrade = security.verify_password(password, user.password)
    if not ok:
        return None
    if need_upgrade:
        user.password = security.get_hash_password(password)
        await db.commit()
        await db.refresh(user)
    return user
#token验证用户
async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
#更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    #字典解包
    #没有设置的字段，则不更新
    query = update(User).where(User.username == username).values(**user_data.model_dump(exclude_unset=True, exclude_none=True))
    result = await db.execute(query)
    await db.commit()
    #检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    updated_user = await get_user_by_username(db, username)
    return updated_user
#修改密码:验证旧密码，小密码加密，修改密码
async def change_password(db: AsyncSession,user: User, username: str, old_password: str, new_password: str):
    ok, _ = security.verify_password(old_password, user.password)
    if not ok:
        return False
    hashed_new_password = security.get_hash_password(new_password)
    query = update(User).where(User.username == username).values(password=hashed_new_password)
    db.add(user)#sqlAlchemy真正接管user对象，规避掉数据库关闭或者异常
    result = await db.execute(query)
    await db.commit()
    await db.refresh(user)
    return True