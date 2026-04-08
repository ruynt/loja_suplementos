from models.produto import Produto
from services.persistencia import Persistencia


class EstoqueService:
    def __init__(self, caminho_produtos):
        self.caminho_produtos = caminho_produtos
        self.produtos = self.carregar_produtos()

    def carregar_produtos(self):
        dados = Persistencia.carregar_dados(self.caminho_produtos)
        return [Produto.from_dict(produto) for produto in dados]

    def salvar_produtos(self):
        dados = [produto.to_dict() for produto in self.produtos]
        Persistencia.salvar_dados(self.caminho_produtos, dados)

    def gerar_novo_id(self):
        if not self.produtos:
            return 1
        return max(produto.id_produto for produto in self.produtos) + 1

    def cadastrar_produto(self, nome, categoria, preco, quantidade_estoque):
        novo_produto = Produto(
            self.gerar_novo_id(),
            nome,
            categoria,
            preco,
            quantidade_estoque
        )
        self.produtos.append(novo_produto)
        self.salvar_produtos()
        return novo_produto

    def listar_produtos(self):
        return self.produtos

    def buscar_produto_por_id(self, id_produto):
        for produto in self.produtos:
            if produto.id_produto == id_produto:
                return produto
        return None

    def buscar_produtos_por_nome(self, nome):
        nome = nome.lower()
        return [produto for produto in self.produtos if nome in produto.nome.lower()]

    def atualizar_produto(self, id_produto, nome=None, categoria=None, preco=None, quantidade_estoque=None):
        produto = self.buscar_produto_por_id(id_produto)
        if produto:
            if nome:
                produto.nome = nome
            if categoria:
                produto.categoria = categoria
            if preco is not None:
                produto.atualizar_preco(preco)
            if quantidade_estoque is not None:
                if quantidade_estoque < 0:
                    raise ValueError("A quantidade em estoque não pode ser negativa.")
                produto.quantidade_estoque = quantidade_estoque

            self.salvar_produtos()
            return True
        return False

    def remover_produto(self, id_produto):
        produto = self.buscar_produto_por_id(id_produto)
        if produto:
            self.produtos.remove(produto)
            self.salvar_produtos()
            return True
        return False