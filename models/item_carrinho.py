class ItemCarrinho:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_subtotal(self):
        return self.produto.preco * self.quantidade

    def __str__(self):
        return (
            f"{self.produto.nome} | "
            f"Qtd: {self.quantidade} | "
            f"Subtotal: R$ {self.calcular_subtotal():.2f}"
        )