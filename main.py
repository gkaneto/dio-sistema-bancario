import time
from datetime import date

INTERVAL = 1
MENU = '''
*******************************
*                             *
*  Escolha uma opção:         * 
*                             *
*  [D] Depositar              *
*  [S] Sacar                  *
*  [E] Extrato                *
*  [Q] Sair                   *
*                             *
*******************************
'''


class Conta:
    def __init__(self, nome = 'Fulano', saldo = 0):
        self.nome = nome
        self.saldo = saldo
        self.limites = Limites()
        self.extrato = Extrato()
    
    def depositar(self):
        valor = float(input('Quanto deseja depositar? R$ '))
        self.saldo += valor
        self.extrato.adicionar(date.today(), 'D', valor)
        print(f'Depósito realizado no valor de R$ {valor:.2f}')
        print('')
        time.sleep(INTERVAL)

    def sacar(self):
        # se não houver saques, voltar ao menu
        s = self.limites.saques_hoje(self.extrato)
        saques_disponiveis = self.limites.saque_qtd - s[0]
        if saques_disponiveis <= 0:
            print('Você não tem mais saques disponíveis hoje!')
            return
            
        # mostrar saques disponíveis
        print(f'Você tem {saques_disponiveis} {"saques disponíveis" if saques_disponiveis > 1 else "saque disponível"} hoje.')

        # se houver: perguntar valor
        while True:
            valor = float(input('Quanto deseja sacar? R$ '))
            if valor > self.saldo:
                # comparar com saldo
                print(f'Saldo indisponível!')
                print('')
                break
            elif valor > self.limites.saque_valor:
                # checar valor limite por saque
                print(f'Seu limite por saque é R$ {self.limites.saque_valor:.2f}')
                print('')
            elif s[1]+valor > self.limites.saque_valor_diario:
                # chear valor limite diário de saque
                print(f'Você já sacou R$ {s[1]:.2f} hoje e seu limite diário é R$ {self.limites.saque_valor_diario:.2f}.')
                print(f'Você pode sacar no máximo R$ {(self.limites.saque_valor_diario - s[1]):.2f}')
                print('')
            else:
                # atualizar saldo e lançar no extrato
                self.saldo -= valor
                self.extrato.adicionar(date.today(), 'S', (-valor))
                print(f'Saque realizado no valor de R$ {valor:.2f}')
                print('')    
                time.sleep(INTERVAL)
                break

class Limites:
    def __init__(self, saque_valor = 500, saque_qtd = 3, saque_valor_diario = 1000):
        self.saque_valor = saque_valor
        self.saque_qtd = saque_qtd
        self.saque_valor_diario = saque_valor_diario

    def saques_hoje(self, extrato):
        # retorna (qtd_saques, valor_total)
        s = [v for d, t, v in extrato.movimentacoes if (d == date.today() and t == 'S')]
        print(f'Saques hoje: {(len(s), -sum(s))}')
        return (len(s), -sum(s))

class Extrato:
    def __init__(self):
        # movimentações no formato (dia, tipo, valor)
        self.movimentacoes = []
    
    def adicionar(self, dia, tipo, valor):
        self.movimentacoes.append((dia, tipo, valor))


    def mostrar(self):
        largura = 40
        col1 = 12
        col2 = 8
        col3 = 16
        saldo = f'R$ {sum([v for d,t,v in self.movimentacoes]):.2f}'

        print(" EXTRATO ".center(largura,'='))
        if self.movimentacoes == []:
            print('')
            print(" Não foram realizadas movimentações ".center(largura))
            print('')
        else:
            for d,t,v in self.movimentacoes:
                print(f' {str(d).ljust(col1)} {t.ljust(col2)} {f"{v:.2f}".rjust(col3)}')
            print(f" {' '.ljust(col1)} {' '.rjust(col2)} {''.rjust(col3,'-')}")

        print(f" {' '.ljust(col1)} {'SALDO'.rjust(col2)} {saldo.rjust(col3)}")
        print(''.center(largura,'='))
        print('')
        input('Aperte Enter para continuar')

def hoje():
    return True

def menu():
    print(MENU)
    while True:
        opcao = input('Digite a opção desejada: ').strip().upper()
        print('')
        if opcao in ['D', 'S', 'E', 'Q']:
            return opcao
        else:
            print('Opção inválida. Tente novamente.')
            time.sleep(INTERVAL)


def main():
    conta = Conta()
    while True:
        op = menu()
        if op == 'D':
            conta.depositar()
            print(f'Saldo atual: R$ {conta.saldo:.2f}')
        elif op == 'S':
            conta.sacar()
            print(f'Saldo atual: R$ {conta.saldo:.2f}')
        elif op == 'E':
            # mostrar extrato
            conta.extrato.mostrar()
        elif op == 'Q':
            print("Até logo! Obrigado por usar nosso Banco!")
            time.sleep(INTERVAL)
            break
        time.sleep(INTERVAL)


        
            
main()
