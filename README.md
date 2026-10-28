## Integrantes

- Fernando Washington
- João Victor Carrenho

## Como rodar

```bash
pip install -r requirements.txt
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
  schemas.py         # modelos do Pydantic
  db.py              # dados em memória
  routers/
    consulta.py      # GET e POST
    edicao.py        # PUT e DELETE
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
