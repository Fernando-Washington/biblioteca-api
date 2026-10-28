import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import app

client = TestClient(app)

LIVRO = {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899}


@pytest.fixture(autouse=True)
def limpar_banco():
    db.livros.clear()
    db.proximo_id = 1


def test_criar_livro():
    resposta = client.post("/livros/", json=LIVRO)
    assert resposta.status_code == 201
    assert resposta.json()["id"] == 1


def test_criar_livro_invalido():
    resposta = client.post("/livros/", json={**LIVRO, "ano": -1})
    assert resposta.status_code == 422


def test_listar_com_filtro():
    client.post("/livros/", json=LIVRO)
    client.post("/livros/", json={**LIVRO, "autor": "Outro Autor"})
    resposta = client.get("/livros/", params={"autor": "machado"})
    assert len(resposta.json()) == 1


def test_buscar_livro():
    client.post("/livros/", json=LIVRO)
    assert client.get("/livros/1").status_code == 200
    assert client.get("/livros/99").status_code == 404


def test_atualizar_livro():
    client.post("/livros/", json=LIVRO)
    resposta = client.put("/livros/1", json={**LIVRO, "titulo": "Esaú e Jacó"})
    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Esaú e Jacó"
    assert client.put("/livros/99", json=LIVRO).status_code == 404


def test_remover_livro():
    client.post("/livros/", json=LIVRO)
    assert client.delete("/livros/1").status_code == 204
    assert client.get("/livros/1").status_code == 404
    assert client.delete("/livros/1").status_code == 404
