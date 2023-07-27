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
segundos_i = 0
segundos_f = 0


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
    multiplicatorio = 0
    #faz a multiplicação
    multiplicatorio = (dirichlet[0]**(alfa[0]-1))*(dirichlet[1]**(alfa[1]-1))*(dirichlet[2]**(alfa[2]-1))
    return(multiplicatorio)

#matriz covariância 2d
def covar(alfa):
    #cria um vetor com as variancias
    vetor = scipy.stats.dirichlet.var(alfa)
    #cria uma matriz de tamanho requirido
    matriz = np.identity(2)
    soma = np.sum(alfa)
    #monta a matriz covariancia
    for k in range(0,2):
        for l in range(0,2):
            if (k == l):
                matriz[k][k] = vetor[k]
            else: matriz[k][l] = -1*alfa[k]*alfa[l]/((soma**2)*(soma + 1))
    return(matriz)

#gerador de valores da distribuicao alvo
def distribu(pot ,alfa, posicao):
    contador = 0
    potencial_atual = pot
    potencial_prox = 0
    atual = posicao
    aceitos = []
    divi = 0
    auxiliar = 2
    ajuda = 0

    while (contador != 3855000):
        #gerando valores normais (empiricamente, o dobro de valores é suficiente, se não for, ele gera mais 3855000 para o vetor)
        #a geração dessa forma é mais rápida, apesar de poder gerar um excesso  de valores
        normal = np.random.multivariate_normal([0,0],cov = covariancia, size = 3855000*auxiliar)
        ajuda = 0
        while (ajuda < 3855000*auxiliar and contador != 3855000):      
            #somando com os anteriores e colocando no simplex
            proximo = [(atual[0]+normal[ajuda][0]),(atual[1]+normal[ajuda][1]),1-(atual[0]+normal[ajuda][0]+atual[1]+normal[ajuda][1])]
            ajuda = ajuda + 1
            #calculando a potencial desse proximo valor
            potencial_prox = potencial(proximo,alfa)
            #realizandoa divisão pra comparação
            divi = potencial_prox/potencial_atual
            #verifica se os valores são positivos
            if(proximo[0] > 0 and proximo[1] > 0 and proximo [2] > 0):
                #se for maior que um aceita automaticamente, se for menor verifique se aceita ou não
                if (divi < 1):
                    if(divi < np.random.uniform()):
                        pass
                    else:
                        contador = contador + 1
                        if(contador > 5000):aceitos.append(potencial_prox)
                        atual = proximo
                        potencial_atual = potencial_prox
                else:
                    contador = contador + 1
                    if(contador > 5000):aceitos.append(potencial_prox)
                    atual = proximo
                    potencial_atual = potencial_prox
        auxiliar = 1        
    return(aceitos)



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

#calculando a matriz covariância
covariancia = covar(alpha)

#gerando os thetas dirichlet
print("Gerando os valores, aguarde...\n")
segundos_i = time.time()
#vetor inicial [1/3,1/3,1/3] faz parte da distribuição alvo, foi escolhido de forma aleatoria para dar inicio
valores = distribu(potencial([1/3,1/3,1/3],alpha),alpha,[1/3,1/3,1/3])
segundos_f = time.time()
tempo = segundos_f-segundos_i
print("O tempo que passou na geração dos valores é: %.1f segundos\n" %tempo)

#ordena o vetor de valores da função
valores = sorted(valores)

#criando as divisões
for contador in range(1540,3850001,1540):
    quantidade.append(valores[contador-1540:contador])
    fronteira.append(quantidade[auxiliar][1540-1])
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
        aproximacao = 1540*k
        #checagem do número interior ao corte
        if(k != 2500):
            aproximacao = aproximacao + np.searchsorted(quantidade[k], V*beta)

        #mostrando o valor de U
        resultado = aproximacao/3850000
        print("U(",V,") = ", end="")
        print("%.4f\n" %resultado)