#queremos integrar a função e^(-ax)*cos(bx) entre 0 e 1.
#sendo a = 0.557072566 e b = 0.46553151806

import numpy as np 
from scipy.stats import qmc
import scipy

#escolha
print("1 - HIT OR MISS")
print("2 - CRUDE")
print("3 - IMPORTANCE")
print("4 - CONTROL")
print("5 - TODAS (1-2-3-4 RESPECTIVAMENTE)")

#fazendo a escolha
escolha = int(input("Escolha o tipo de cálculo: "))

#definindo a seed para a replicação do projeto
sampler = qmc.Halton(d=2,seed = 1)

#função somatorio de X
def somatorio(vetor, contador):
    auxiliar = []
    if(contador > 1):
        #deixando o vetor ordenado, visto que nesse caso é sempre decrescente
        vetor.sort()
        for k in range(1,contador):
            auxiliar.append(np.sqrt((vetor[k-1] - vetor[k-2])**2))
    return(np.sum(auxiliar))

#definindo funções
def hit_or_miss():
    print("Método Hit Or Miss")
    #variaveis
    contador = 0 
    estimativa = 0
    contador_interior_area = 0
    funcao = 0

    #esse while roda ao menos 35000, o motivo está no relatório
    while (contador < 35000):
        contador = contador + 1
        #gerando x com a função Halton
        x = sampler.random()
        #calculando a função no ponto
        funcao = np.exp((x[0][0])*-0.557072566)*np.cos((x[0][0])*0.46553151806)

        if (funcao >= (x[0][1])):
            #analisa se os valores gerados fazem parte da circunferencia
            contador_interior_area = contador_interior_area + 1
            estimativa = contador_interior_area/contador

    print("O valor estimado é: ", estimativa)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa)/0.74303)
    print("")
    return 0

def crude():
    print("Método Crude")
    
    #variaveis
    contador = 0 
    estimativa = 0
    areas = []
    vetor_x = []
    discrepancia = 0
    funcao = 0
    auxiliar = 0

    #esse while roda ao menos 10 vezes com a intenção de criar um cálculo inicial do erro
    while (contador < 10) or (0.0005*estimativa < (discrepancia*auxiliar)):
        contador = contador + 1
        #gerando a variavel com distribuição quasi random halton
        x = sampler.random()
        #adicionando valor a um vetor para futuras operações
        vetor_x.append(x[0])
        #operações com o x
        funcao = np.exp((x[0][0])*-0.557072566)*np.cos((x[0][0])*0.46553151806)
        #adicionando a função num vetor
        areas.append(funcao)
        #calculado a discrepancia o valor da variação (auxiliar) e a estimativa
        discrepancia = qmc.discrepancy(vetor_x)
        estimativa = np.mean(areas)
        auxiliar = auxiliar + somatorio(areas,contador)

    print("O valor estimado é: ", estimativa)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa)/0.74303356)
    print("")

    return 0

def importance():
    print("Método Importance Sampling")
    #variaveis
    contador = 0 
    estimativa = 0
    vetor_x = []

    #esse while roda ao menos 6152 vezes, o motivo está no relatório
    while ((contador < 6152)):
        contador = contador + 1
        #gerando a variavel halton (uniforme)
        x =  sampler.random()
        #inserindo o valor x em um vetor
        vetor_x.append(x[0])
        #tranformando a uniforme em Beta
        b = scipy.stats.beta.ppf(x[0][0],1,1.25)
        #função f e densidade escolhida g
        f = np.exp(b*-0.557072566)*np.cos(b*0.46553151806)
        g = 1.25*((1-b)**0.25)
        #adicionando a função num vetor
        estimativa = estimativa + (f/g)

    print("O valor estimado é: ", estimativa/contador)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa/contador)/0.74303356)
    print("")   
    return 0

def control():
    print("Método Control Variable")

    #variaveis
    vetor_x = []
    estimativa = 0
    contador = 0
    controle_num = 0
    integral = 0.721463717
    discrepancia = 0
    vetor = []
    auxiliar = 0

    #esse while roda ao menos 100 vezes com a intenção de criar um cálculo inicial do erro
    while ((contador <= 100) or ((0.0005*estimativa/contador < discrepancia*auxiliar))):
        contador = contador + 1
        #gerando a variável halton(uniforme)
        x = sampler.random()
        #calculando o valor da função f e do controle numérico
        f = np.exp((x[0][0])*-0.557072566)*np.cos((x[0][0])*0.46553151806)
        controle_num = 1-(0.557072566*(x[0][0]))
        #fazendo cálculo de estimativa
        estimativa = estimativa + (f-controle_num + integral)
        #adicionando valor num vetor para cálculos futuros
        vetor.append(f-controle_num + integral)
        #adicionando valor x[0] num vetor para cálculos futuros
        vetor_x.append(x[0])
        #calculando a discrepancia
        discrepancia = qmc.discrepancy(vetor_x)
        #calculando valor auxiliar
        auxiliar = auxiliar + somatorio(vetor,contador)

    print("O valor estimado é: ", estimativa/contador)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa/contador)/0.74303356)
    print("")   
    return 0

if(escolha == 1):
    sampler = qmc.Halton(d=2,seed = 13686431)
    hit_or_miss()
    
if(escolha == 2):
    sampler = qmc.Halton(d=1,seed = 13686431)
    crude()

if(escolha == 3):
    sampler = qmc.Halton(d=1,seed = 13686431)
    importance()

if(escolha == 4):
    sampler = qmc.Halton(d=1,seed = 13686431)
    control()

if(escolha == 5):
    hit_or_miss()
    sampler = qmc.Halton(d=1,seed = 13686431)
    crude()
    sampler = qmc.Halton(d=1,seed = 13686431)
    importance()
    sampler = qmc.Halton(d=1,seed = 13686431)
    control()

