from fastapi import FastAPI, status, HTTPException, Request
from app.database.database import Base, get_db, Engine
from app.models.book import *
from app.services.services import create_response
from app.routers.book import books_router
from fastapi.exceptions import RequestValidationError


app = FastAPI()
app.include_router(books_router)
Base.metadata.create_all(bind=Engine)


@app.get("/health")
def check_health():

    return {
        "message": "API đang chạy",
        "data": None
    }


# global exception
@app.exception_handler(HTTPException)
def except_httpexception_handler(req: Request, exc: HTTPException):

    return create_response(
        req=req,
        statusCode=exc.status_code,
        message=exc.detail,
        error=exc.detail
    )


@app.exception_handler(RequestValidationError)
def except_request_handler(req: Request, exc: RequestValidationError):
    return create_response(
        req=req,
        statusCode=status.HTTP_422_UNPROCESSABLE_CONTENT,
        message=str(exc),
        error=str(exc)
    )


@app.exception_handler(Exception)
def general_exception_handler(req: Request, exc: Exception):
    return create_response(
        req=req,
        statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Có lỗi từ hệ thống",
        error=str(exc)
    )
