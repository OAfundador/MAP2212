#importando as bibliotecas
import numpy as np 
import scipy
import time

#variáveis
escolha_usuario = 0
vetor_x = []
vetor_y = []
alpha = []
dirichi = 0
contador = 0
auxiliar = 0
valores = []
fronteira = []
quantidade = []
beta = 0
aproximacao = 0
V = 0


"""
Definindo funções utilizadas
"""
#função caso o usuario queria colocar o vetor:
def usuario():
    #colocação das váriaveis X pelo usuário
    print("Variáveis X (Naturais) \n")
    vetor_x.append(int(input("Insira a primeira variável X: ")))
    vetor_x.append(int(input("Insira a segunda variável X: ")))
    vetor_x.append(int(input("Insira a terceira variável X: ")))
    print("\n")

    #colocação das váriaveis Y pelo usuário
    print("Variáveis Y (Naturais) \n")
    vetor_y.append(int(input("Insira a primeira variável Y: ")))
    vetor_y.append(int(input("Insira a segunda variável Y: ")))
    vetor_y.append(int(input("Insira a terceira variável Y: ")))

#função potencial
def potencial(dirichlet, alfa):
    return(dirichlet[0]**(alfa[0]-1))*(dirichlet[1]**(alfa[1]-1))*(dirichlet[2]**(alfa[2]-1))

"""""
Programa principal
"""""
#pergunta se o usario quer um especifico ou se o usario quer colocar estes valores:
print("\n")
escolha_usuario = int(input("Digite 0 se quiser utilizar o vetor de variaveis a priori já definido. \nDigite 1 se quiser colocar os proprios valores no vetor.\nValor: "))
if(escolha_usuario == 1):
    usuario()
else: 
    vetor_x.append(4)
    vetor_x.append(6)
    vetor_x.append(4)
    vetor_y.append(1)
    vetor_y.append(2)
    vetor_y.append(3)

#mostrando os vetores iniciais:
print("\n")
print("O vetor X é",vetor_x, "o vetor Y é",vetor_y)

#definindo a seed utilizada 
np.random.seed(13686431)

#definindo alpha
alpha.append(vetor_y[0] + vetor_x[0])
alpha.append(vetor_y[1] + vetor_x[1])
alpha.append(vetor_y[2] + vetor_x[2])

#constante de normalização
beta = (((scipy.special.gamma(alpha[0]))*(scipy.special.gamma(alpha[1]))*(scipy.special.gamma(alpha[2])))/(scipy.special.gamma(alpha[0]+alpha[1]+alpha[2])))

#gerando os thetas dirichlet
print("Gerando os valores, aguarde...\n")
dirichlet = np.random.dirichlet(alpha, size=15375000)

#fazendo virar uma potencial e os colocando um vetor
for contador in range(15375000):   
    dirichi = (potencial(dirichlet[contador], alpha))
    valores.append(dirichi)
contador = 0

#ordena o vetor de valores da função
valores = sorted(valores)

#criando as divisões
for contador in range(6150,15375001,6150):
    quantidade.append(valores[contador-6150:contador])
    fronteira.append(quantidade[auxiliar][6150-1])
    auxiliar = auxiliar + 1

#mostra o maior valor
maior = fronteira[2499]/beta
print("O maior valor é: %.4f \n" %maior)

#solicitação ao usuario um valor V
while(True):
    print("Caso queira encerrar o programa insira um número menor que 0")
    V = float(input("Insira um valor de V (maior igual a zero): "))
    if(V < 0):
        break
    else:
        k = np.searchsorted(fronteira, V*beta)
        #quantidade de números até o corte
        aproximacao = 6150*k
        #checagem do número interior ao corte
        if(k != 2500):
            aproximacao = aproximacao + np.searchsorted(quantidade[k], V*beta)
        #mostrando o valor de U
        resultado = aproximacao/15375000
        print("U(",V,") = ", end="")
        print("%.4f\n" %resultado)


