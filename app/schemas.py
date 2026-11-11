from pydantic import BaseModel, ConfigDict, Field


class LivroCriar(BaseModel):
    """Dados de entrada (POST e PUT)."""

    titulo: str = Field(min_length=1, max_length=100, examples=["Dom Casmurro"])
    autor: str = Field(min_length=1, max_length=100, examples=["Machado de Assis"])
    ano: int = Field(ge=0, le=2100, examples=[1899])
    disponivel: bool = True


class Livro(LivroCriar):
    """Dados de saída: o livro com o id gerado."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class UsuarioCriar(BaseModel):
    email: str = Field(min_length=3, max_length=100, examples=["admin@biblioteca.com"])
    senha: str = Field(min_length=4, max_length=50, examples=["123456"])


class Usuario(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
