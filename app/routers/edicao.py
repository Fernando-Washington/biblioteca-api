from fastapi import APIRouter, HTTPException

from app import db
from app.schemas import Livro, LivroCriar

router = APIRouter(prefix="/livros", tags=["livros"])


@router.put("/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro: LivroCriar):
    if livro_id not in db.livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.livros[livro_id] = {"id": livro_id, **livro.model_dump()}
    return db.livros[livro_id]


@router.delete("/{livro_id}", status_code=204)
def remover_livro(livro_id: int):
    if livro_id not in db.livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    del db.livros[livro_id]
