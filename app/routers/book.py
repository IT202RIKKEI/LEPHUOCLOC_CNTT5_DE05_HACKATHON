from fastapi import APIRouter, status, Depends, HTTPException, Request
from app.services.services import *
from sqlalchemy.orm import Session
from app.schemas.book import BookOut, BookCreate, BookUpdate
from app.database.database import get_db

books_router = APIRouter(
    prefix="/books",
    tags=["QUẢN LÝ SÁCH THƯ VIÊN"],
)


# =============================== LẤY TOÀN BỘ DANH SÁCH SÁCH ===============================

@books_router.get("/", status_code=status.HTTP_200_OK)
def get_books(req: Request, db: Session = Depends(get_db)):

    list_books = get_books_sv(db)

    safety_data = [BookOut.model_validate(
        b).model_dump(mode="json") for b in list_books]

    return create_response(req=req, statusCode=200,
                           message="Lấy dữ liệu sách thành công",
                           data=safety_data)

# =============================== END REGION ===============================


# =============================== TÌM THEO CATEGORY ===============================

@books_router.get("/search", status_code=status.HTTP_200_OK)
def get_books_filter(req: Request, db: Session = Depends(get_db), category: str | None = None):

    list_books = get_books_filter_sv(db, category)

    safety_data = [BookOut.model_validate(
        b).model_dump(mode="json") for b in list_books]

    return create_response(req=req, statusCode=200,
                           message="Lấy dữ liệu sách thành công",
                           data=safety_data)


# =============================== END REGION ===============================


# =============================== TÌM THEO ID ===============================

@books_router.get("/{book_id}", status_code=status.HTTP_200_OK)
def get_book(req: Request, book_id: int, db: Session = Depends(get_db)):

    book_data = get_book_sv(db, book_id)

    if book_data == "NOT_EXISTS_BOOK":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sách"
        )

    safety_data = BookOut.model_validate(book_data).model_dump(mode="json")

    return create_response(req=req, statusCode=200,
                           message="Lấy dữ liệu sách thành công",
                           data=safety_data)


# =============================== END REGION ===============================

# =============================== TẠO SÁCH MỚI ===============================
@books_router.post("/", status_code=status.HTTP_201_CREATED)
def new_book(req: Request, book_data: BookCreate, db: Session = Depends(get_db)):

    result_book_data = new_book_sv(db, book_data)

    if result_book_data == "EXISTS_BOOK":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sách có tiêu đề: {book_data.title} đã tồn tại trên hệ thống"
        )
    safety_data = BookOut.model_validate(
        result_book_data).model_dump(mode="json")

    return create_response(req=req, statusCode=201,
                           message="Tạo sách mới thành công!",
                           data=safety_data)


# =============================== END REGION ===============================


# =============================== CẬP NHẬT SÁCH  ===============================
@books_router.put("/{book_id}", status_code=status.HTTP_200_OK)
def update_book(req: Request, inp_upd_data: BookUpdate, book_id: int, db: Session = Depends(get_db)):

    result_book_data = update_book_sv(db, inp_upd_data, book_id)

    if result_book_data == "NOT_EXISTS_BOOK":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy sách"
        )
    safety_data = BookUpdate.model_validate(
        result_book_data).model_dump(mode="json")

    return create_response(req=req, statusCode=200,
                           message=f"Cập nhật sách thành công cho sách có id: {book_id}",
                           data=safety_data)


# =============================== END REGION ===============================

# =============================== XÓA SÁCH ===============================

@books_router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(req: Request, book_id: int, db: Session = Depends(get_db)):

    book_data = delete_book_sv(db, book_id)

    if book_data == "NOT_EXISTS_BOOK":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sách"
        )

    return create_response(req=req, statusCode=200,
                           message="Xóa sách thành công",
                           data=None)


# =============================== END REGION ===============================
