from fastapi import FastAPI

from app.routers import auth, consulta, edicao

app = FastAPI(
    title="Biblioteca API",
    description="API simples para gerenciar livros com persistência em SQLite.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(consulta.router)
app.include_router(edicao.router)

