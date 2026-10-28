# Biblioteca API

API REST simples com FastAPI e Pydantic para gerenciar livros. Os dados ficam em memória (sem banco de dados).

## Integrantes

- Fernando Washington
- (nome do colega)

## Como rodar

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentação (Swagger): http://127.0.0.1:8000/docs

## Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /livros | Lista os livros (filtros `autor` e `disponivel`) |
| GET | /livros/{id} | Busca um livro |
| POST | /livros | Cadastra um livro |
