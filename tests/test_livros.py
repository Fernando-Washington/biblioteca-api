import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.db import Base, get_db
from app.main import app

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(autocommit=False, autoflush=False, bind=engine_teste)
Base.metadata.create_all(bind=engine_teste)


def get_db_teste():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_db_teste
client = TestClient(app)

LIVRO = {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899}
USUARIO = {"email": "teste@biblioteca.com", "senha": "123456"}


@pytest.fixture(autouse=True)
def limpar_banco():
    with SessionTeste() as session:
        session.query(models.Livro).delete()
        session.query(models.Usuario).delete()
        session.commit()


@pytest.fixture
def headers():
    client.post("/usuarios", json=USUARIO)
    resposta = client.post(
        "/token", data={"username": USUARIO["email"], "password": USUARIO["senha"]}
    )
    token = resposta.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}



def test_criar_livro(headers):
    resposta = client.post("/livros/", json=LIVRO, headers=headers)
    assert resposta.status_code == 201
    assert resposta.json()["id"] == 1


def test_criar_livro_invalido(headers):
    resposta = client.post("/livros/", json={**LIVRO, "ano": -1}, headers=headers)
    assert resposta.status_code == 422


def test_listar_com_filtro(headers):
    client.post("/livros/", json=LIVRO, headers=headers)
    client.post("/livros/", json={**LIVRO, "autor": "Outro Autor"}, headers=headers)
    resposta = client.get("/livros/", params={"autor": "machado"})
    assert len(resposta.json()) == 1


def test_buscar_livro(headers):
    client.post("/livros/", json=LIVRO, headers=headers)
    assert client.get("/livros/1").status_code == 200
    assert client.get("/livros/99").status_code == 404


def test_atualizar_livro(headers):
    client.post("/livros/", json=LIVRO, headers=headers)
    resposta = client.put(
        "/livros/1", json={**LIVRO, "titulo": "Esaú e Jacó"}, headers=headers
    )
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Esaú e Jacó"
    assert client.put("/livros/99", json=LIVRO, headers=headers).status_code == 404


def test_remover_livro(headers):
    client.post("/livros/", json=LIVRO, headers=headers)
    assert client.delete("/livros/1", headers=headers).status_code == 204
    assert client.get("/livros/1").status_code == 404
    assert client.delete("/livros/1", headers=headers).status_code == 404


def test_login_senha_errada():
    client.post("/usuarios", json=USUARIO)
    resposta = client.post(
        "/token", data={"username": USUARIO["email"], "password": "errada"}
    )
    assert resposta.status_code == 401


def test_rotas_protegidas_sem_token():
    assert client.post("/livros/", json=LIVRO).status_code == 401
    assert client.put("/livros/1", json=LIVRO).status_code == 401
    assert client.delete("/livros/1").status_code == 401
    assert client.get("/livros/").status_code == 200


def test_token_invalido():
    headers = {"Authorization": "Bearer token-falso"}
    assert client.post("/livros/", json=LIVRO, headers=headers).status_code == 401
