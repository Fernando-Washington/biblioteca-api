from fastapi import APIRouter, HTTPException

from app import db
from app.schemas import Livro, LivroCriar

router = APIRouter(prefix="/livros", tags=["livros"])


@router.get("/", response_model=list[Livro])
def listar_livros(autor: str | None = None, disponivel: bool | None = None):
    """Lista os livros. Filtros opcionais por autor e disponibilidade."""
    resultado = list(db.livros.values())
    if autor is not None:
        resultado = [l for l in resultado if autor.lower() in l["autor"].lower()]
    if disponivel is not None:
        resultado = [l for l in resultado if l["disponivel"] == disponivel]
    return resultado


@router.get("/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    """Busca um livro pelo id."""
    if livro_id not in db.livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db.livros[livro_id]


@router.post("/", response_model=Livro, status_code=201)
def criar_livro(livro: LivroCriar):
    """Cadastra um novo livro."""
    novo = {"id": db.gerar_id(), **livro.model_dump()}
    db.livros[novo["id"]] = novo
    return novo
