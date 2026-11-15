from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.auth import verificar_token
from app.db import get_db
from app.schemas import Livro, LivroCriar

router = APIRouter(prefix="/livros", tags=["livros"])


@router.put(
    "/{livro_id}",
    response_model=Livro,
    summary="Atualizar livro",
    responses={
        404: {"description": "Livro não encontrado"},
        422: {"description": "Dados inválidos"},
    },
)
def atualizar_livro(
    livro_id: int, livro: LivroCriar, session: Session = Depends(get_db)
):
    """
    Atualiza todos os dados de um livro existente.
    """
    registro = session.get(models.Livro, livro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for campo, valor in livro.model_dump().items():
        setattr(registro, campo, valor)
    session.commit()
    session.refresh(registro)
    return registro


@router.delete(
    "/{livro_id}",
    status_code=204,
    summary="Remover livro",
    responses={
        401: {"description": "Token inválido ou ausente"},
        404: {"description": "Livro não encontrado"},
    },
    dependencies=[Depends(verificar_token)],
)
def remover_livro(livro_id: int, session: Session = Depends(get_db)):
    """
    Remove um livro pelo id.

    Precisa enviar o token no header **X-Token**.
    """
    registro = session.get(models.Livro, livro_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    session.delete(registro)
    session.commit()
