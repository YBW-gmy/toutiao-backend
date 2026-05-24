from fastapi import HTTPException
from utils.exception import http_exception_handler,integrity_error_handler,sqlalchemy_error_handler,general_exception_handler
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError

def register_exception_handlers(app):
    #注册全局异常处理，子类在前父类在后
    app.add_exception_handler(HTTPException, http_exception_handler)#业务报错
    app.add_exception_handler(IntegrityError,integrity_error_handler)#数据完整性
    app.add_exception_handler(SQLAlchemyError,sqlalchemy_error_handler)#数据类
    app.add_exception_handler(Exception,general_exception_handler)#兜底