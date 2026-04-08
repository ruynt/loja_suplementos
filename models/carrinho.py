from models.item_carrinho import ItemCarrinho


class Carrinho:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, produto, quantidade):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        if quantidade > produto.quantidade_estoque:
            raise ValueError("Estoque insuficiente para esse produto.")

        for item in self.itens:
            if item.produto.id_produto == produto.id_produto:
                nova_quantidade = item.quantidade + quantidade
                if nova_quantidade > produto.quantidade_estoque:
                    raise ValueError("Quantidade total no carrinho excede o estoque disponível.")
                item.quantidade = nova_quantidade
                return

        self.itens.append(ItemCarrinho(produto, quantidade))

    def remover_item(self, id_produto):
        for item in self.itens:
            if item.produto.id_produto == id_produto:
                self.itens.remove(item)
                return True
        return False

    def listar_itens(self):
        return self.itens

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens)

    def esta_vazio(self):
        return len(self.itens) == 0

    def limpar_carrinho(self):
        self.itens.clear()