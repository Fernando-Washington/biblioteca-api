from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import Livro, LivroCriar

router = APIRouter(prefix="/livros", tags=["livros"])


@router.get("/", response_model=list[Livro], summary="Listar livros")
def listar_livros(
    autor: str | None = None,
    disponivel: bool | None = None,
    session: Session = Depends(get_db),
):
    """
    Retorna todos os livros cadastrados.

    - **autor**: filtra pelo nome do autor (busca parcial, sem diferenciar maiúsculas)
    - **disponivel**: filtra por livros disponíveis ou não
    """
    query = session.query(models.Livro)
    if autor is not None:
        query = query.filter(models.Livro.autor.ilike(f"%{autor}%"))
    if disponivel is not None:
        query = query.filter(models.Livro.disponivel == disponivel)
    return query.all()


@router.get(
    "/{livro_id}",
    response_model=Livro,
    summary="Buscar livro por id",
    responses={404: {"description": "Livro não encontrado"}},
)
def buscar_livro(livro_id: int, session: Session = Depends(get_db)):
    """
    Retorna os dados de um livro a partir do seu id.
    """
    livro = session.get(models.Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.post(
    "/",
    response_model=Livro,
    status_code=201,
    summary="Cadastrar livro",
    responses={422: {"description": "Dados inválidos"}},
)
def criar_livro(livro: LivroCriar, session: Session = Depends(get_db)):
    """
    Cadastra um novo livro.

    O id é gerado automaticamente. Título e autor são obrigatórios
    e o ano deve estar entre 0 e 2100.
    """
    novo = models.Livro(**livro.model_dump())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo
