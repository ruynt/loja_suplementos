from models.carrinho import Carrinho
from models.pedido import Pedido
from services.estoque_service import EstoqueService
from services.persistencia import Persistencia
from utils.validacoes import validar_texto, validar_preco, validar_quantidade, validar_id


CAMINHO_PRODUTOS = "data/produtos.json"
CAMINHO_PEDIDOS = "data/pedidos.json"


def exibir_menu():
    print("\n" + "=" * 50)
    print("      SISTEMA DE VENDAS - LOJA DE SUPLEMENTOS")
    print("=" * 50)
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Buscar produto por nome")
    print("4 - Atualizar produto")
    print("5 - Remover produto")
    print("6 - Adicionar produto ao carrinho")
    print("7 - Visualizar carrinho")
    print("8 - Remover item do carrinho")
    print("9 - Finalizar pedido")
    print("10 - Ver pedidos realizados")
    print("0 - Sair")
    print("=" * 50)


def cadastrar_produto(estoque):
    try:
        nome = validar_texto(input("Nome do produto: "), "nome")
        categoria = validar_texto(input("Categoria: "), "categoria")
        preco = validar_preco(input("Preço: "))
        quantidade = validar_quantidade(input("Quantidade em estoque: "))

        produto = estoque.cadastrar_produto(nome, categoria, preco, quantidade)
        print(f"Produto cadastrado com sucesso: {produto}")
    except ValueError as e:
        print(f"Erro: {e}")


def listar_produtos(estoque):
    produtos = estoque.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\nProdutos cadastrados:")
    for produto in produtos:
        print(produto)


def buscar_produto(estoque):
    try:
        nome = validar_texto(input("Digite o nome do produto: "), "nome")
        produtos = estoque.buscar_produtos_por_nome(nome)

        if not produtos:
            print("Nenhum produto encontrado.")
            return

        print("\nProdutos encontrados:")
        for produto in produtos:
            print(produto)
    except ValueError as e:
        print(f"Erro: {e}")


def atualizar_produto(estoque):
    try:
        id_produto = validar_id(input("ID do produto a atualizar: "))
        produto = estoque.buscar_produto_por_id(id_produto)

        if not produto:
            print("Produto não encontrado.")
            return

        print("Deixe em branco caso não queira alterar algum campo.")

        nome = input(f"Novo nome ({produto.nome}): ").strip()
        categoria = input(f"Nova categoria ({produto.categoria}): ").strip()
        preco_input = input(f"Novo preço ({produto.preco}): ").strip()
        quantidade_input = input(f"Nova quantidade em estoque ({produto.quantidade_estoque}): ").strip()

        preco = None
        quantidade = None

        if preco_input:
            preco = validar_preco(preco_input)
        if quantidade_input:
            quantidade = validar_quantidade(quantidade_input)

        estoque.atualizar_produto(
            id_produto,
            nome=nome if nome else None,
            categoria=categoria if categoria else None,
            preco=preco,
            quantidade_estoque=quantidade
        )

        print("Produto atualizado com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")


def remover_produto(estoque):
    try:
        id_produto = validar_id(input("ID do produto a remover: "))
        if estoque.remover_produto(id_produto):
            print("Produto removido com sucesso.")
        else:
            print("Produto não encontrado.")
    except ValueError as e:
        print(f"Erro: {e}")


def adicionar_ao_carrinho(estoque, carrinho):
    try:
        id_produto = validar_id(input("ID do produto: "))
        produto = estoque.buscar_produto_por_id(id_produto)

        if not produto:
            print("Produto não encontrado.")
            return

        quantidade = validar_quantidade(input("Quantidade: "))
        if quantidade == 0:
            print("A quantidade deve ser maior que zero.")
            return

        carrinho.adicionar_item(produto, quantidade)
        print("Produto adicionado ao carrinho com sucesso.")
    except ValueError as e:
        print(f"Erro: {e}")


def visualizar_carrinho(carrinho):
    if carrinho.esta_vazio():
        print("O carrinho está vazio.")
        return

    print("\nItens no carrinho:")
    for item in carrinho.listar_itens():
        print(item)

    print(f"Total: R$ {carrinho.calcular_total():.2f}")


def remover_do_carrinho(carrinho):
    try:
        id_produto = validar_id(input("ID do produto a remover do carrinho: "))
        if carrinho.remover_item(id_produto):
            print("Item removido do carrinho.")
        else:
            print("Item não encontrado no carrinho.")
    except ValueError as e:
        print(f"Erro: {e}")


def gerar_novo_id_pedido():
    pedidos = Persistencia.carregar_dados(CAMINHO_PEDIDOS)
    if not pedidos:
        return 1
    return max(pedido["id_pedido"] for pedido in pedidos) + 1


def finalizar_pedido(estoque, carrinho):
    if carrinho.esta_vazio():
        print("Não é possível finalizar um pedido com o carrinho vazio.")
        return

    try:
        for item in carrinho.listar_itens():
            if item.quantidade > item.produto.quantidade_estoque:
                raise ValueError(f"Estoque insuficiente para o produto {item.produto.nome}.")

        for item in carrinho.listar_itens():
            item.produto.remover_estoque(item.quantidade)

        estoque.salvar_produtos()

        pedido = Pedido(
            id_pedido=gerar_novo_id_pedido(),
            itens=carrinho.listar_itens(),
            valor_total=carrinho.calcular_total()
        )

        pedidos = Persistencia.carregar_dados(CAMINHO_PEDIDOS)
        pedidos.append(pedido.to_dict())
        Persistencia.salvar_dados(CAMINHO_PEDIDOS, pedidos)

        print("Pedido finalizado com sucesso.")
        print(pedido)

        carrinho.limpar_carrinho()

    except ValueError as e:
        print(f"Erro ao finalizar pedido: {e}")


def ver_pedidos():
    pedidos = Persistencia.carregar_dados(CAMINHO_PEDIDOS)
    if not pedidos:
        print("Nenhum pedido registrado.")
        return

    print("\nPedidos realizados:")
    for pedido in pedidos:
        print("-" * 50)
        print(f"Pedido #{pedido['id_pedido']}")
        print(f"Data: {pedido['data']}")
        print(f"Total: R$ {pedido['valor_total']:.2f}")
        print("Itens:")
        for item in pedido["itens"]:
            print(
                f"  - {item['nome']} | "
                f"Qtd: {item['quantidade']} | "
                f"Preço unit.: R$ {item['preco_unitario']:.2f} | "
                f"Subtotal: R$ {item['subtotal']:.2f}"
            )


def main():
    estoque = EstoqueService(CAMINHO_PRODUTOS)
    carrinho = Carrinho()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(estoque)
        elif opcao == "2":
            listar_produtos(estoque)
        elif opcao == "3":
            buscar_produto(estoque)
        elif opcao == "4":
            atualizar_produto(estoque)
        elif opcao == "5":
            remover_produto(estoque)
        elif opcao == "6":
            adicionar_ao_carrinho(estoque, carrinho)
        elif opcao == "7":
            visualizar_carrinho(carrinho)
        elif opcao == "8":
            remover_do_carrinho(carrinho)
        elif opcao == "9":
            finalizar_pedido(estoque, carrinho)
        elif opcao == "10":
            ver_pedidos()
        elif opcao == "0":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()