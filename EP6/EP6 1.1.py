#importando as bibliotecas
import numpy as np 
import scipy


#função potencial
def potencial(dirichlet, alfa):
    return((dirichlet[0]**(alfa[0]-1))*(dirichlet[1]**(alfa[1]-1))*(dirichlet[2]**(alfa[2]-1)))

#hipótese
def hip(x):
    return -(potencial([x, 1-(x + ((1 - np.sqrt(x))**2)),(1 - np.sqrt(x))**2], ajudante))

#função verdade
def werdade(V,fronteira,beta,quantidade):
     if(V < 0):
        return (-1)
     else:
        k = np.searchsorted(fronteira, V*beta)
        #quantidade de números até o corte
        aproximacao = 1540*k
        #checagem do número interior ao corte
        if(k != 2500):
            aproximacao = aproximacao + np.searchsorted(quantidade[k], V*beta)
        #mostrando o valor de U
        resultado = aproximacao/3850000
        return(resultado)

#função de e-valor padronizado
def std_e(e_v):
    #dimensões dadas
    t = 2
    h = 1
    df = t-h
    #calculando o e-valor barra
    e_v_b = 1 - e_v
    #calculando qq barra
    qq_b = scipy.stats.chi2.cdf(scipy.stats.chi2.ppf(e_v_b, t),df)
    #calculando qq
    qq = 1 - qq_b
    return(qq)

#função corpo
def corpo(vetor_x,vetor_y):

    alpha = []
    dirichi = 0
    contador = 0
    auxiliar = 0
    valores = []
    fronteira = []
    quantidade = []
    beta = 0
    e_valor = 0
    std = 0

    #mostrando os vetores iniciais:
    print("\n")
    print("O vetor X é",vetor_x, "o vetor Y é",vetor_y)

    #definindo a seed utilizada 
    np.random.seed(13686431)

    #definindo alpha
    alpha.append(vetor_y[0] + vetor_x[0])
    alpha.append(vetor_y[1] + vetor_x[1])
    alpha.append(vetor_y[2] + vetor_x[2])

    #auxiliar especifico para maximizar a hipótese
    global ajudante
    ajudante = alpha

    #constante de normalização
    beta = (((scipy.special.gamma(alpha[0]))*(scipy.special.gamma(alpha[1]))*(scipy.special.gamma(alpha[2])))/(scipy.special.gamma(alpha[0]+alpha[1]+alpha[2])))

    #gerando os thetas dirichlet
    print("Gerando os valores, aguarde...\n")
    dirichlet = np.random.dirichlet(alpha, size=3850000)

    #fazendo virar uma potencial e os colocando um vetor
    for contador in range(3850000):   
        dirichi = (potencial(dirichlet[contador], alpha))
        valores.append(dirichi)
    contador = 0

    #ordena o vetor de valores da função
    valores = sorted(valores)

    #criando as divisões
    for contador in range(1540,3850001,1540):
        quantidade.append(valores[contador-1540:contador])
        fronteira.append(quantidade[auxiliar][1540-1])
        auxiliar = auxiliar + 1

    #mostra o maior valor
    #print("O maior valor é de: ",fronteira[2499]/beta,"\n")

    #maximizando a hipótese
    res = scipy.optimize.minimize_scalar(fun = hip, bounds=(0.0, 1.0), method='bounded')
    #print("O s* é: ",-res.fun/beta)

    #calcula a função verdade W do e-valor
    e_valor = werdade(-res.fun/beta,fronteira,beta,quantidade)
    #print("O e-valor(H|X) é: ",e_valor)

    #calculando e-valor padronizado
    std = std_e(e_valor)
    #print("o std", std_e(e_valor))

    #testa a hipótese
    if(std < 0.05):
        print("Hipótese rejeitada")
        return(0)
    else: 
        print("Hipótese não rejeitada")
        return(1)
    
#vetores x e vetore y
vx = [[1,17,2], [1,16, 3], [1,15, 4], [1,14, 5], [1,13,6], [1,12, 7], [1,11, 8], [1,10, 9], [1,9, 10], [1,8, 11], [1,7, 12], [1,6, 13], [1,5, 14], [1,4, 15], [1,3, 16], [1,2, 17], [1,1, 18], [5,14, 1], [5,13, 2], [5,12, 3], [5,11, 4], [5,10, 5], [5,9, 6], [5,8 ,7], [5,7, 8], [5,6, 9], [5,5, 10], [9,10, 1], [9,9, 2], [9,8, 3], [9,7, 4], [9,6, 5], [9,5, 6], [9,4, 7]]
vy = [[0,0,0],[1,1,1]]

#variaveis auxiliares
cont = 0
tipo_0 = 0
tipo_1 = 0
k = 0
#calculando a quantidade total e de cada tipo de hipóteses aceitas
for k in range(len(vx)):
    j = 0
    for j in range(2):
        cont = cont + 1
        if (j == 0):
            tipo_0 = tipo_0 + corpo(vx[k],vy[j])
        else: tipo_1 = tipo_1 + corpo(vx[k],vy[j])

print("Foram não rejeitados", tipo_0 + tipo_1 ,"do total de", cont)
print("Foram não rejeitados", tipo_0, "quando o vetor Y é",vy[0])
print("Foram não rejeitados", tipo_1, "quando o vetor Y é",vy[1])

