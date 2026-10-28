# "Banco" em memória: os dados somem quando o servidor reinicia.
livros: dict[int, dict] = {}
proximo_id = 1


def gerar_id() -> int:
    global proximo_id
    novo = proximo_id
    proximo_id += 1
    return novo
