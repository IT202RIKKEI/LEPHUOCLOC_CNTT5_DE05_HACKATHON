from fastapi.responses import JSONResponse
from fastapi import Request
from datetime import datetime, timezone
from typing import Any
from sqlalchemy.orm import Session
from app.models.book import BookModel
from app.schemas.book import BookCreate, BookUpdate

# =============================== TẠO 6 TRƯỜNG DỮ LIỆU ===============================


def create_response(req: Request,
                    statusCode: int,
                    error: Any | None = None,
                    message: str | None = None,
                    data: Any | None = None,):

    body_content = {
        "statusCode": statusCode,
        "message": message,
        "data": data,
        "error": error,
        "timestampt": datetime.now().isoformat(),
        "path": req.url.path
    }

    return JSONResponse(
        status_code=statusCode,
        content=body_content
    )

# =============================== END REGION ===============================

# =============================== LẤY DANH SÁCH SÁCH ===============================


def get_books_sv(db: Session):

    list_books = db.query(BookModel).all()

    return list_books

# =============================== END REGION ===============================


# =============================== LẤY DANH SÁCH THEO CATEGORY ===============================
def get_books_filter_sv(db: Session, category: str | None = None):
    query = db.query(BookModel)

    if category:
        query = query.filter(
            BookModel.category.ilike(f"%{category}%"))

    return query.all()

# =============================== END REGION ===============================


# =============================== LẤY sách theo ID ===============================
def get_book_sv(db: Session, book_id: int):

    book_data = db.query(BookModel).filter(
        BookModel.id == book_id).first()

    if not book_data:
        return "NOT_EXISTS_BOOK"

    return book_data
# =============================== END REGION ===============================


# =============================== TẠO SÁCH MỚI ===============================
def new_book_sv(db: Session, book_data: BookCreate):

    # kiểm tra tựa đề đã tồn tại chưa
    exists_book = db.query(BookModel).filter(
        BookModel.title == book_data.title).first()

    if exists_book:
        return "EXISTS_BOOK"

    # CH THÌ TẠO
    main_book_data = BookModel(**book_data.model_dump(mode="json"))

    try:
        db.add(main_book_data)
        db.commit()
        db.refresh(main_book_data)

        return main_book_data
    except Exception as e:
        db.rollback()
        raise e

# =============================== END REGION ===============================


# =============================== CẬP NHẬT SÁCH  ===============================
def update_book_sv(db: Session, inp_upd_data: BookUpdate, book_id: int):

    # kiểm sách có tồn tại không
    update_book = db.query(BookModel).filter(
        BookModel.id == book_id).first()

    if not update_book:
        return "NOT_EXISTS_BOOK"

    update_data = inp_upd_data.model_dump(mode="json")

    for k, v in update_data.items():
        setattr(update_book, k, v)
    try:
        db.commit()

        return update_data
    except Exception as e:
        db.rollback()
        raise e

# =============================== END REGION ===============================


# =============================== XÓA sách theo ID ===============================
def delete_book_sv(db: Session, book_id: int):

    book_data = db.query(BookModel).filter(
        BookModel.id == book_id).first()

    if not book_data:
        return "NOT_EXISTS_BOOK"

    try:
        db.delete(book_data)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
# =============================== END REGION ===============================
