from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    autor: Mapped[str] = mapped_column(String(100), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
