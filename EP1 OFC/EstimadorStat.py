import random
import numpy as np


contador = 0 
estimativa = 0
contador_interior_circulo = 0

#enquanto o valor da variavel não estiver entre esses parametros o programa vai continuar rodando indefinidamente
#esse while roda ao menos 1000 vezes com a intenção de criar um cálculo inicial do desvio padrão

while ((contador < 1000) or (not(0.0005*estimativa/2 >= np.sqrt((estimativa*(1-estimativa)/contador))))):
    #geração de coordenadas aleatorias
    contador = contador + 1
    random.seed(contador*1368)
    x = random.random()
    random.seed(contador*6431)
    y = random.random()
    
    if (x*x + y*y <= 1):
        #analisa se os valores gerados fazem parte da circunferencia
        contador_interior_circulo = contador_interior_circulo + 1
        estimativa = contador_interior_circulo/contador
        
print("O valor de PI estimado é: ", 4*estimativa)
print("N = ", contador)
print("A precisão em relação ao PI conhecido é: ",(estimativa*4/3.14159265359))

