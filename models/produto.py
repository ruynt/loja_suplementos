class Produto:
    def __init__(self, id_produto, nome, categoria, preco, quantidade_estoque):
        self.id_produto = id_produto
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def adicionar_estoque(self, quantidade):
        self.quantidade_estoque += quantidade

    def remover_estoque(self, quantidade):
        if quantidade > self.quantidade_estoque:
            raise ValueError("Quantidade solicitada maior que o estoque disponível.")
        self.quantidade_estoque -= quantidade

    def atualizar_preco(self, novo_preco):
        if novo_preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        self.preco = novo_preco

    def to_dict(self):
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade_estoque": self.quantidade_estoque
        }

    @staticmethod
    def from_dict(dados):
        return Produto(
            dados["id_produto"],
            dados["nome"],
            dados["categoria"],
            dados["preco"],
            dados["quantidade_estoque"]
        )

    def __str__(self):
        return (
            f"ID: {self.id_produto} | "
            f"Nome: {self.nome} | "
            f"Categoria: {self.categoria} | "
            f"Preço: R$ {self.preco:.2f} | "
            f"Estoque: {self.quantidade_estoque}"
        )