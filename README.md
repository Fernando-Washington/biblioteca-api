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
  models.py          # modelos ORM (tabelas livros e usuarios)
  seguranca.py       # hash de senha, geração e validação do JWT
  schemas.py         # modelos do Pydantic
  routers/
    auth.py          # cadastro de usuário e login (/token)
    consulta.py      # GET e POST
    edicao.py        # PUT e DELETE
alembic/
  env.py             # configuração do ambiente de migração
  versions/          # scripts de migração do banco
tests/
  test_livros.py
```


## Rotas

| Método | Rota | Descrição | Autenticação |
|--------|------|-----------|--------------|
| POST | /usuarios | Cadastra um usuário (e-mail e senha) | Não |
| POST | /token | Login, devolve o token JWT | Não |
| GET | /livros | Lista os livros (filtros `autor` e `disponivel`) | Não |
| GET | /livros/{id} | Busca um livro | Não |
| POST | /livros | Cadastra um livro | Sim |
| PUT | /livros/{id} | Atualiza um livro | Sim |
| DELETE | /livros/{id} | Remove um livro | Sim |

## Autenticação

A senha do usuário é salva com hash (bcrypt, via Passlib). O login em `/token` segue o padrão OAuth2 com senha e devolve um token JWT que vale 30 minutos. As rotas POST, PUT e DELETE de livros exigem esse token no header `Authorization: Bearer <token>`. As rotas GET são públicas.

A chave usada para assinar o token pode ser definida pela variável de ambiente `SECRET_KEY`.

### Testando pelo Swagger

1. Rode o projeto e abra http://127.0.0.1:8000/docs
2. Em `POST /usuarios`, cadastre um usuário:

```json
{
  "email": "admin@biblioteca.com",
  "senha": "123456"
}
```

3. Clique no botão **Authorize** (cadeado no topo da página), informe o e-mail no campo `username`, a senha no campo `password` e clique em **Authorize**.
4. Pronto, as rotas POST, PUT e DELETE de `/livros` já podem ser usadas. Sem fazer o login elas retornam `401`.

### Testando pelo terminal

```bash
curl -X POST http://127.0.0.1:8000/token -d "username=admin@biblioteca.com&password=123456"
```

Resposta:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBiaWJsaW90ZWNhLmNvbSIsImV4cCI6MTc5NDM3NTE0MX0.5VfwWxkApJACRzDf40z4lq37flKzCzXu6fKUpwjkbI0",
  "token_type": "bearer"
}
```

Usando o token para cadastrar um livro:

```bash
curl -X POST http://127.0.0.1:8000/livros/   -H "Authorization: Bearer <token>"   -H "Content-Type: application/json"   -d '{"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899}'
```

