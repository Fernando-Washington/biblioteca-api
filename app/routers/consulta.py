from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import Livro, LivroCriar
from app.seguranca import get_usuario_atual

router = APIRouter(prefix="/livros", tags=["livros"])


@router.get("/", response_model=list[Livro])
def listar_livros(
    autor: str | None = None,
    disponivel: bool | None = None,
    session: Session = Depends(get_db),
):
    """Lista os livros. Filtros opcionais por autor e disponibilidade."""
    query = session.query(models.Livro)
    if autor is not None:
        query = query.filter(models.Livro.autor.ilike(f"%{autor}%"))
    if disponivel is not None:
        query = query.filter(models.Livro.disponivel == disponivel)
    return query.all()


@router.get("/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int, session: Session = Depends(get_db)):
    """Busca um livro pelo id."""
    livro = session.get(models.Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.post("/", response_model=Livro, status_code=201)
def criar_livro(
    livro: LivroCriar,
    session: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual),
):
    """Cadastra um novo livro."""
    novo = models.Livro(**livro.model_dump())
    session.add(novo)
    session.commit()
    session.refresh(novo)
    return novo

