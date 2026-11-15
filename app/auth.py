from fastapi import Header, HTTPException

TOKEN = "segredo123"


def verificar_token(x_token: str | None = Header(default=None)):
    if x_token != TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido ou ausente")
