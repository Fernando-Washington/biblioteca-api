from fastapi import FastAPI

from app.routers import consulta

app = FastAPI(
    title="Biblioteca API",
    description="API simples para gerenciar livros (dados em memória).",
    version="1.0.0",
)

app.include_router(consulta.router)
