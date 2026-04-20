import traceback

from fastapi import HTTPException,Request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from starlette import status
from starlette.responses import JSONResponse

DEBUG_MODE = True

async def http_exception_handler(request:Request,exc:HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code":exc.status_code,
                "message":exc.detail,
                "data":None
            }
        )
async def sqlalchemy_exception_handler(request:Request,exc:SQLAlchemyError):
    error_data=None
    if DEBUG_MODE:
        error_data = {
            "error_type":type(exc).__name__,
            "error_detail":str(exc),
            "traceback":traceback.format_exc(),
            "path":str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"数据库操作失败，请稍后重试",
            "data":error_data
        }
    )
async def general_exception_handler(request:Request,exc:Exception):
    error_data=None
    if DEBUG_MODE:
        error_data = {
            "error_type": type(exc).__name__,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
            "path": str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":500,
            "message":"服务器内部错误",
            "data":error_data
        }
    )

