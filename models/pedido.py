from datetime import datetime


class Pedido:
    def __init__(self, id_pedido, itens, valor_total, data=None):
        self.id_pedido = id_pedido
        self.itens = itens
        self.valor_total = valor_total
        self.data = data if data else datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def to_dict(self):
        return {
            "id_pedido": self.id_pedido,
            "data": self.data,
            "valor_total": self.valor_total,
            "itens": [
                {
                    "id_produto": item.produto.id_produto,
                    "nome": item.produto.nome,
                    "quantidade": item.quantidade,
                    "preco_unitario": item.produto.preco,
                    "subtotal": item.calcular_subtotal()
                }
                for item in self.itens
            ]
        }

    def __str__(self):
        return f"Pedido #{self.id_pedido} | Data: {self.data} | Total: R$ {self.valor_total:.2f}"