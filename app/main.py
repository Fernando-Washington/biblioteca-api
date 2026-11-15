from fastapi import FastAPI

from app.routers import consulta, edicao

tags = [
    {"name": "livros", "description": "Operações para consultar, cadastrar, atualizar e remover livros."},
]

app = FastAPI(
    title="Biblioteca API",
    description="API para gerenciar livros com persistência em SQLite.",
    version="1.0.0",
    openapi_tags=tags,
)

app.include_router(consulta.router)
app.include_router(edicao.router)
