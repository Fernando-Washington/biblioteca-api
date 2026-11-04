from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import Livro, LivroCriar

router = APIRouter(prefix="/livros", tags=["livros"])


@router.put("/{livro_id}", response_model=Livro)
def atualizar_livro(
    livro_id: int, livro: LivroCriar, session: Session = Depends(get_db)
):
    registro = session.get(models.Livro, livro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for campo, valor in livro.model_dump().items():
        setattr(registro, campo, valor)
    session.commit()
    session.refresh(registro)
    return registro


@router.delete("/{livro_id}", status_code=204)
def remover_livro(livro_id: int, session: Session = Depends(get_db)):
    registro = session.get(models.Livro, livro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    session.delete(registro)
    session.commit()

