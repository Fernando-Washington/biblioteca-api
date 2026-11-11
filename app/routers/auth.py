from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models
from app.db import get_db
from app.schemas import Token, Usuario, UsuarioCriar
from app.seguranca import criar_token, gerar_hash, verificar_senha

router = APIRouter(tags=["auth"])


@router.post("/usuarios", response_model=Usuario, status_code=201)
def cadastrar_usuario(dados: UsuarioCriar, session: Session = Depends(get_db)):
    existe = session.query(models.Usuario).filter_by(email=dados.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    usuario = models.Usuario(email=dados.email, senha_hash=gerar_hash(dados.senha))
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario


@router.post("/token", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)
):
    usuario = session.query(models.Usuario).filter_by(email=form.username).first()
    if usuario is None or not verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": criar_token(usuario.email), "token_type": "bearer"}
