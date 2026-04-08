def validar_texto(texto, nome_campo):
    texto = texto.strip()
    if not texto:
        raise ValueError(f"O campo {nome_campo} não pode estar vazio.")
    return texto


def validar_preco(valor):
    try:
        preco = float(valor)
        if preco <= 0:
            raise ValueError
        return preco
    except ValueError:
        raise ValueError("Preço inválido. Digite um número maior que zero.")


def validar_quantidade(valor):
    try:
        quantidade = int(valor)
        if quantidade < 0:
            raise ValueError
        return quantidade
    except ValueError:
        raise ValueError("Quantidade inválida. Digite um número inteiro maior ou igual a zero.")


def validar_id(valor):
    try:
        id_produto = int(valor)
        if id_produto <= 0:
            raise ValueError
        return id_produto
    except ValueError:
        raise ValueError("ID inválido. Digite um número inteiro positivo.")