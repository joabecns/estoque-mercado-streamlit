import json
import os

ARQUIVO = "estoque.json"
LIMITE_ESTOQUE_BAIXO = 10

ESTOQUE_PADRAO = {
    "1":  {"nome": "arroz",          "preco": 25.9,  "quantidade": 50},
    "2":  {"nome": "feijão",         "preco": 8.5,   "quantidade": 80},
    "3":  {"nome": "leite integral", "preco": 5.2,   "quantidade": 120},
    "4":  {"nome": "óleo de soja",   "preco": 7.8,   "quantidade": 60},
    "5":  {"nome": "açúcar",         "preco": 4.9,   "quantidade": 100},
    "6":  {"nome": "macarrão",       "preco": 3.5,   "quantidade": 75},
    "7":  {"nome": "café",           "preco": 14.9,  "quantidade": 40},
    "8":  {"nome": "farinha",        "preco": 4.2,   "quantidade": 87},
    "9":  {"nome": "sabão em pó",    "preco": 11.5,  "quantidade": 8},
    "10": {"nome": "chocolate",      "preco": 5.0,   "quantidade": 5},
}


def carregar_estoque() -> dict:
    """Carrega o estoque do arquivo JSON. Se não existir, cria com os dados padrão."""
    if not os.path.exists(ARQUIVO):
        salvar_estoque(ESTOQUE_PADRAO)
        return dict(ESTOQUE_PADRAO)

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_estoque(estoque: dict) -> None:
    """Persiste o dicionário de estoque no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)


def proximo_id(estoque: dict) -> str:
    """Retorna o próximo ID inteiro disponível como string."""
    if not estoque:
        return "1"
    ids_numericos = [int(k) for k in estoque.keys() if k.isdigit()]
    return str(max(ids_numericos) + 1)


def adicionar_item(estoque: dict, nome: str, preco: float, quantidade: int) -> tuple[dict, str, str]:
    """
    Adiciona ou atualiza um produto no estoque.
    Retorna (estoque_atualizado, status, mensagem).
    status pode ser 'adicionado' ou 'atualizado'.
    """
    nome = nome.strip().lower()

    # Verifica se produto já existe pelo nome
    id_existente = None
    for id_prod, dados in estoque.items():
        if dados["nome"] == nome:
            id_existente = id_prod
            break

    if id_existente:
        estoque[id_existente] = {"nome": nome, "preco": preco, "quantidade": quantidade}
        salvar_estoque(estoque)
        return estoque, "atualizado", f"Produto '{nome.title()}' atualizado com sucesso (ID: {id_existente})."
    else:
        novo_id = proximo_id(estoque)
        estoque[novo_id] = {"nome": nome, "preco": preco, "quantidade": quantidade}
        salvar_estoque(estoque)
        return estoque, "adicionado", f"Produto '{nome.title()}' adicionado com sucesso (ID: {novo_id})."


def remover_item(estoque: dict, id_produto: str) -> tuple[dict, str]:
    """
    Remove um produto pelo ID.
    Retorna (estoque_atualizado, mensagem).
    """
    if id_produto not in estoque:
        return estoque, f"ID '{id_produto}' não encontrado no estoque."

    nome = estoque[id_produto]["nome"].title()
    del estoque[id_produto]
    salvar_estoque(estoque)
    return estoque, f"Produto '{nome}' removido com sucesso."


def produtos_estoque_baixo(estoque: dict) -> list[dict]:
    """Retorna lista de produtos com quantidade abaixo do limite."""
    alertas = []
    for id_prod, dados in estoque.items():
        if dados["quantidade"] < LIMITE_ESTOQUE_BAIXO:
            alertas.append({
                "id": id_prod,
                "nome": dados["nome"].title(),
                "quantidade": dados["quantidade"],
                "preco": dados["preco"],
            })
    return sorted(alertas, key=lambda x: x["quantidade"])
