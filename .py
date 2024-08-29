from datetime import datetime
import json

# tratamento de exceçoes
class EstacionamentoException(Exception):
    pass

class QuantidadeInvalidaException(EstacionamentoException):
    def __init__(self, message="Inválido. Deve ser um número inteiro maior que zero."):
        super().__init__(message)

class VagasInsuficientesException(EstacionamentoException):
    def __init__(self, message="Não há vagas suficientes para adicionar tantos carros."):
        super().__init__(message)

class CarrosInsuficientesException(EstacionamentoException):
    def __init__(self, message="Não há carros suficientes no estacionamento."):
        super().__init__(message)

# classe paraa gerir o estacionamento
class Estacionamento:
    def __init__(self):
        self.carros = 0  
        self.vagas_totais = 150  
        self.vagas_disponiveis = self.vagas_totais  
        self.transacoes = []  

    # funçao para adicionar carros no estacionamento
    def adicionar_carro(self, quantidade):
        try:
            self.validar_quantidade(quantidade)  
            if self.vagas_disponiveis < quantidade:
                raise VagasInsuficientesException(f"Apenas {self.vagas_disponiveis} vagas disponiveis. Não é possível adicionar {quantidade} carros.")
            self.carros += quantidade
            self.vagas_disponiveis -= quantidade
            self.registrar_transacao("adicionados", quantidade) 
        except QuantidadeInvalidaException as e:
            print(f"Erro ao adicionar carros: {e}")
        except VagasInsuficientesException as e:
            print(f"Erro ao adicionar carros: {e}")

    # funçao para remover carros do estacionamento
    def retirar_carro(self, quantidade):
        try:
            self.validar_quantidade(quantidade)  
            if self.carros < quantidade:
                raise CarrosInsuficientesException(f"Apenas {self.carros} carros no estacionamento. Não é possivel retirar {quantidade} carros.")
            self.carros -= quantidade
            self.vagas_disponiveis += quantidade
            self.registrar_transacao("retirados", quantidade)  
        except QuantidadeInvalidaException as e:
            print(f"Erro ao retirar carros: {e}")
        except CarrosInsuficientesException as e:
            print(f"Erro ao retirar carros: {e}")

    # funcao para mostrar todas as transaçoes feitas
    def mostrar_transacoes(self):
        print("\nRegistro de Transaçõs:")
        for transacao in self.transacoes:
            print(f"{transacao['Data/Hora']} - {transacao['Mensagem']}")

    # funcao para validaçao de quanttidade
    def validar_quantidade(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise QuantidadeInvalidaException()

    # funçao para registrar transaçoes
    def registrar_transacao(self, tipo, quantidade):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"{quantidade} carros {tipo} ao estacionamento."
        transacao = {"Data/Hora": data_hora, "Mensagem": mensagem}
        self.transacoes.append(transacao)

# funcao para puxar o arquivo json
def mostrar_informacoes_json():
    try:
        with open('informações.json', 'r') as arquivo_json:
            informacoes = json.load(arquivo_json)
            print("\nInformações do Estacionamento:\n")
            print(f"{informacoes['nome_estacionamento']}")
            print(f"Endereço: {informacoes['endereço']}\n")
            print("Contato:")
            print(f" Telefone: {informacoes['contato']['telefone']}")
            print(f" Email: {informacoes['contato']['email']}")
    except FileNotFoundError:
        print("\nArquivo 'informacoes.json' não encontrado.")
    except json.JSONDecodeError:
        print("\nErro ao decodificar o arquivo JSON.")

# funcao para mostrar menu
def menu():
    print("\n=============== Menu ===============")
    print("1 - Adicionar Carros")
    print("2 - Retirar Carros")
    print("3 - Mostrar Transações")
    print("4 - Mostrar Informações do Estacionamento")
    print("5 - Sair")
    print(f"Vagas disponiveis: {estacionamento.vagas_disponiveis}/{estacionamento.vagas_totais}")

# funcao para pedir ao usuario para escolher uma opçao
def escolher_opcao():
    while True:
        try:
            opcao = int(input("\nEscolha uma opção: "))
            if 1 <= opcao <= 5:
                return opcao
            else:
                print("Opção inválida. Tente de novo.")
        except ValueError:
            print("Insira um número inteiro válido.")

# inicia uma nova instancia de estacionamento
estacionamento = Estacionamento()

# loop do programa
while True:
    menu()
    opcao = escolher_opcao()

    if opcao == 1:
        while True:
            try:
                quantidade = int(input("\nDigite a quantidade de carros a serem adicionados: "))
                estacionamento.adicionar_carro(quantidade)
                break
            except EstacionamentoException as e:
                print(f"Erro: {e}")
                break  
    elif opcao == 2:
        while True:
            try:
                quantidade = int(input("\nDigite a quantidade de carros a serem retirados: "))
                estacionamento.retirar_carro(quantidade)
                break
            except EstacionamentoException as e:
                print(f"Erro: {e}")
                break  
    elif opcao == 3:
        estacionamento.mostrar_transacoes()
    elif opcao == 4:
        mostrar_informacoes_json()
    elif opcao == 5:
        print("\nSaindo do programa.")
        break
    else:
        print("\nOpção inválida. Escolha de novo.")
