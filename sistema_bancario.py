from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
            return False

        self.saldo = self.saldo - valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        
        self.saldo = self.saldo + valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = 0
        for transacao in self.historico.transacoes:
            if transacao["tipo"] == "Saque":
                numero_saques = numero_saques + 1

        if valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
            return False

        if numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
            return False

        return super().sacar(valor)


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        nova_transacao = {
            "tipo": transacao.tipo,
            "valor": transacao.valor,
            "data": data_hora
        }
        self.transacoes.append(nova_transacao)


class Transacao:
    def __init__(self, valor):
        self.valor = valor
        self.tipo = ""

    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        super().__init__(valor)
        self.tipo = "Saque"

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__(valor)
        self.tipo = "Deposito"

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


def mostrar_menu():
    print("\n================ MENU ================")
    print("[d] Depositar")
    print("[s] Sacar")
    print("[e] Extrato")
    print("[nc] Nova conta")
    print("[lc] Listar contas")
    print("[nu] Novo usuário")
    print("[q] Sair")
    opcao = input("=> ")
    return opcao


def encontrar_cliente(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def pegar_conta_cliente(cliente):
    if len(cliente.contas) == 0:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    return cliente.contas[0]


def fazer_deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente is None:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except:
        print("\n@@@ Valor inválido! @@@")
        return

    conta = pegar_conta_cliente(cliente)
    if conta is None:
        return

    deposito = Deposito(valor)
    cliente.realizar_transacao(conta, deposito)


def fazer_saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente is None:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except:
        print("\n@@@ Valor inválido! @@@")
        return

    conta = pegar_conta_cliente(cliente)
    if conta is None:
        return

    saque = Saque(valor)
    cliente.realizar_transacao(conta, saque)


def mostrar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente is None:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = pegar_conta_cliente(cliente)
    if conta is None:
        return

    print("\n================ EXTRATO ================")
    
    if len(conta.historico.transacoes) == 0:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in conta.historico.transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - {transacao['data']}")

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    
    # Verifica se já existe
    if encontrar_cliente(cpf, clientes) is not None:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(novo_cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontrar_cliente(cpf, clientes)

    if cliente is None:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    numero_conta = len(contas) + 1
    nova_conta = ContaCorrente(numero_conta, cliente)
    
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    if len(contas) == 0:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        print("=" * 50)
        print(f"Agência: {conta.agencia}")
        print(f"Conta: {conta.numero}")
        print(f"Titular: {conta.cliente.nome}")
        print(f"CPF: {conta.cliente.cpf}")
        print(f"Saldo: R$ {conta.saldo:.2f}")


def main():
    clientes = []
    contas = []

    while True:
        opcao = mostrar_menu()

        if opcao == "d":
            fazer_deposito(clientes)
        elif opcao == "s":
            fazer_saque(clientes)
        elif opcao == "e":
            mostrar_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Obrigado por usar nosso sistema!")
            break
        else:
            print("Operação inválida! Tente novamente.")


if __name__ == "__main__":
    main()
