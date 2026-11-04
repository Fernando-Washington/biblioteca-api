## Integrantes

- Fernando Washington
- João Victor Carrenho

## Como rodar

```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Testes

```bash
pytest
```

## Estrutura

```
app/
  main.py            # criação do app e rotas
  db.py              # configuração do SQLAlchemy/SQLite e sessão (get_db)
  models.py          # modelo ORM (tabela livros)
  schemas.py         # modelos do Pydantic
  routers/
    consulta.py      # GET e POST
    edicao.py        # PUT e DELETE
alembic/
  env.py             # configuração do ambiente de migração
  versions/          # scripts de migração do banco
tests/
  test_livros.py
```


## Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /livros | Lista os livros (filtros `autor` e `disponivel`) |
| GET | /livros/{id} | Busca um livro |
| POST | /livros | Cadastra um livro |
| PUT | /livros/{id} | Atualiza um livro |
| DELETE | /livros/{id} | Remove um livro |

