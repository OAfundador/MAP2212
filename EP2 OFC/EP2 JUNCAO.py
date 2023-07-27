#queremos integrar a função e^(-ax)*cos(bx) entre 0 e 1.
#sendo a = 0.557072566 e b = 0.46553151806

import random
import numpy as np 
import statistics
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
random.seed(13686431)

#definindo funções
def hit_or_miss():
    print("Método Hit Or Miss")
    #variaveis
    contador = 0 
    estimativa = 0
    contador_interior_area = 0
    #esse while roda ao menos 1000 vezes com a intenção de criar um cálculo inicial do desvio padrão
    while ((contador < 1000) or (not(0.0005*estimativa/2 > np.sqrt((estimativa*(1-estimativa)/contador))))):
        contador = contador + 1
        #gerando x,y coordenadas aleatorios uniforme de 0 a 1
        x = random.random()
        y = random.random()

        if (np.exp(x*-0.557072566)*np.cos(x*0.46553151806) >= y):
            #analisa se os valores gerados fazem parte da área
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
    areas = 0
    quad_areas = 0
    dp = 0
    #esse while roda ao menos 1000 vezes com a intenção de criar um cálculo inicial do desvio padrão
    while ((contador <= 1000) or (not(0.0005*estimativa/2 > dp/np.sqrt(contador)))):
        contador = contador + 1
        #gerando x aleatorio uniforme de 0 a 1
        x = random.random()
        
        #adicionando o valor da função em variaveis para futuras operações
        f = np.exp(x*-0.557072566)*np.cos(x*0.46553151806)
        areas = areas + f
        quad_areas = quad_areas + (f**2)
        
        #fazendo a estimativa e o desvio padrão
        estimativa = areas/contador
        dp = np.sqrt((quad_areas/contador) - (estimativa)**2)

    print("O valor estimado é: ", estimativa)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa)/0.74303)
    print("")
    return 0

def importance():
    print("Método Importance Sampling")
    #variaveis
    contador = 0 
    quad_areas = 0
    estimativa = 0
    areas = 0
    dp = 0
    #esse while roda ao menos 1000 vezes com a intenção de criar um cálculo inicial do desvio padrão
    while ((contador < 1000) or (not(0.0005*estimativa > 2*(dp/np.sqrt(contador))))):
        contador = contador + 1
        #gerando um x com distribuição beta
        x = random.betavariate(1,1.25)

        #função f e densidade escolhida g
        f = np.exp(x*-0.557072566)*np.cos(x*0.46553151806)
        g = 1.25*((1-x)**0.25)

        #adicionando a relação de f e g a um vetor para futuras operações
        quad_areas = quad_areas + ((f/g)**2)
        areas = areas + (f/g)

        #fazendo o cálculo do desvio padrão
        estimativa = areas/contador
        dp = np.sqrt((quad_areas/contador) - (estimativa)**2)


        
    print("O valor estimado é: ", estimativa)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa)/0.74303)
    print("")
    return 0

def control():
    print("Método Control Variable")
    #variaveis
    estimativa = 0
    contador = 0
    var = 0
    funcao = []
    controle_num = 0
    controle = []
    integral = 0.721463717
    #esse while roda ao menos 100 vezes com a intenção de criar um cálculo inicial do desvio padrão
    while ((contador <= 100) or (not(0.0005*estimativa/contador) > 2*(np.sqrt(var/contador)))):
        contador = contador + 1
        ##gerando um x com distribuição uniforme 
        x = random.random()
        
        #fazendo o cálculo da função no ponto x
        f = np.exp(x*-0.557072566)*np.cos(x*0.46553151806)

        #fazendo um cálculo da aproximação da função no ponto x
        controle_num = 1-(0.557072566*x)

        #adicionando os valores em vetores para futuras operações
        funcao.append(f)
        controle.append(controle_num)

        #adicionando os valores para o cálculo da estimativa
        estimativa = estimativa + (f-controle_num + integral)
        
        if(contador % 10 == 0):
            #fazendo o cálculo da variancia
            var = statistics.variance(funcao) + statistics.variance(controle) - (2*statistics.covariance(funcao, controle))
        
    print("O valor estimado é: ", estimativa/contador)
    print("N = ", contador)
    print("O valor em relação a integral calculada via Symbolab é: ", (estimativa/contador)/0.74303)
    print("")

if(escolha == 1):
    hit_or_miss()

if(escolha == 2):
    crude()

if(escolha == 3):
    importance()

if(escolha == 4):
    control()

if(escolha == 5):
    hit_or_miss()
    random.seed(13686431)
    crude()
    random.seed(13686431)
    importance()
    random.seed(13686431)
    control()

