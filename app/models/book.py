from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base


class BookModel(Base):

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
