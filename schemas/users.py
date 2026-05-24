from pydantic import BaseModel
from pydantic import Field

from pydantic.config import ConfigDict
from typing import Optional
from pydantic import Field


class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
   nickname: Optional[str] = Field(None, description="昵称")
   avatar: Optional[str] = Field(None, description="头像URl")
   gender: Optional[str] = Field(None, description="性别")
   bio: Optional[str] = Field(None, description="个人简介")




#user_info对应的类
class UserInfoResponse(UserInfoBase):
    id:int
    username: str
    model_config = ConfigDict(from_attributes=True )

#data 数据类型
class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoResponse=Field(...,alias='userInfo')
    #模型类配置
    model_config = ConfigDict(from_attributes=True,populate_by_name=True)
#更新用户信息
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URl")
    gender: Optional[str] = Field(None, description="性别")
    bio: Optional[str] = Field(None, description="个人简介")
    phone: Optional[str] = Field(None, description="手机号")
#修改密码
class UserChangePasswordRequest(BaseModel):
    old_password: str=Field(...,alias="oldPassword",description="旧密码")
    new_password: str=Field(...,alias="newPassword",description="新密码")