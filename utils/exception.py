import traceback
from fastapi import HTTPException,Request
from starlette import status
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from fastapi.responses import JSONResponse
#开发模式：返回详细错误
#生产模式：返回简化的错误
DEBUG_MODe=True
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code":exc.status_code,"message":exc.detail,"data":None}
    )
async def integrity_error_handler(request: Request, exc: IntegrityError):
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code":status.HTTP_400_BAD_REQUEST,"message":str(exc),"data":None}
    )
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    traceback.print_exc()
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":str(exc),"data":None}
    )
async def general_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    if DEBUG_MODe:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":str(exc),"data":None}
        )
    else:
      return JSONResponse(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          content={"code":status.HTTP_500_INTERNAL_SERVER_ERROR,"message":"服务器错误","data":None}
      )