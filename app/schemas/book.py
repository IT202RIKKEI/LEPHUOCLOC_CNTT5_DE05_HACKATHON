from pydantic import BaseModel, Field, ConfigDict, field_validator
from fastapi import HTTPException, status


class BookCreate(BaseModel):

    title: str = Field(
        min_length=3, description="Nhập vào tiêu đề sách giả hợp lệ")
    author: str = Field(
        min_length=3, description="Nhập vào tên tác giả hợp lệ")
    category: str = Field(
        min_length=3, description="Nhập vào tên thể loại hợp lệ")
    quantity: int = Field(ge=0,
                          description="Nhập vào số lượng còn lại hợp lệ")

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BookCreate):
    pass


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    category: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)
