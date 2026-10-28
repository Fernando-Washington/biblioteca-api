from pydantic import BaseModel, Field


class LivroCriar(BaseModel):
    """Dados de entrada (POST e PUT)."""

    titulo: str = Field(min_length=1, max_length=100, examples=["Dom Casmurro"])
    autor: str = Field(min_length=1, max_length=100, examples=["Machado de Assis"])
    ano: int = Field(ge=0, le=2100, examples=[1899])
    disponivel: bool = True


class Livro(LivroCriar):
    """Dados de saída: o livro com o id gerado."""

    id: int
