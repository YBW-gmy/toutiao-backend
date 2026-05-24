from fastapi import APIRouter
from fastapi import Depends
from config.db_config import get_db
from schemas.users import UserRequest
from fastapi import HTTPException
from starlette import status
from models.users import User
from schemas.users import UserUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from crud import users
from schemas.users import UserInfoResponse
from schemas.users import UserAuthResponse
from utils.response import success_response
from utils.auth import get_current_user
from schemas.users import UserInfoBase
from schemas.users import UserChangePasswordRequest
router = APIRouter(prefix="/api/user",tags=["users"])
@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_db)):
    #注册逻辑：验证用户是否存在，不存在则创建用户，生成token，响应结果
    existing_user=await users.get_user_by_username(db,user_data.username)
    if existing_user:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user = await users.create_user(db,user_data)
    user_token= await users.create_token(db,user.id)
    token_str=user_token.token



    response_data=UserAuthResponse(token=token_str,user_info=UserInfoResponse.model_validate(user))
    return success_response(data=response_data)
@router.post("/login")
async def login(user_data: UserRequest,db: AsyncSession = Depends(get_db)):
    #登录逻辑：验证用户是否存在，存在,和密码校验，则生成token，响应结果
    user=await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    user_token= await users.create_token(db,user.id)
    token_str=user_token.token
    response_data=UserAuthResponse(token=token_str,user_info=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功",data=response_data)
#获取token，封装crud,整合成一个工具函数,用户验证
@router.get("/info")
async def get_user_info(user: UserInfoBase =Depends(get_current_user)):

        return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))
#修改用户信息
#参数：验证token，db，用户输入的更新信息
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest,user: User =Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    #更新用户信息
     user=await users.update_user(db,user.username,user_data)
     return success_response(message="更新用户信息成功",data=UserInfoResponse.model_validate(user))
#修改密码
@router.put("/password")
async def update_password(password_data: UserChangePasswordRequest,user: User =Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    res_change_password = await users.change_password(db,user,user.username,password_data.old_password,password_data.new_password)
    if not res_change_password:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="旧密码错误")
    return success_response(message="修改密码成功")