import numpy as np #Utilizada para manipular os vetores
import matplotlib.pyplot as plt #Utilizada para manipular os gráficos
from scipy.integrate import odeint #Utilizada para resolver a EDO
from scipy.optimize import leastsq #Utilizada para ajustar os parâmetros
from math import log #Utilizada para construir os modelos

'''
--------------------------------------------------------------
Matheus Santana dos Santos
Aracaju-SE, junho/2019
Modelagem Matemática - Turma: 01
Departamento de Matemática - Universidade Federal de Sergipe
--------------------------------------------------------------
'''

def modelo_gompertz(p, t, P_infinito, r):
    dpdt = r * p * ( log(P_infinito)-log(p) )
    return dpdt

def residual(p):
    p = tuple(p)
    sim_P = odeint(modelo_gompertz, p0, dados_anos_censo, args=p).flatten()
    res = sim_P - dados_populacao_Brasil
    return res

#Manipula um arquivo externo (de forma simples)
def arquivo(arquivo):
        #Abre o arquivo em modo de leitura
        arq = open(arquivo, 'r')
        txt = arq.read()
        #Separa os valores por '\n'
        txt = txt.split('\n')
        data = []
        for i in range(len(txt)):
                #Separa os valores que contém espaço
                aux = txt[i].split(' ')
                #Inclui os dados na lista
                data.append(int(aux[0])) #Anos | 1º coluna
                data.append(float(aux[1])) #População | 2º coluna
        #Fecha o arquivo
        arq.close()
        return data


dados = arquivo("dados.txt")

# Pega a primeira coluna dos dados que estão no arquivo
dados_anos_censo = dados[0::2]

# Pega a segunda coluna dos dados que estão no arquivo
dados_populacao_Brasil = dados[1::2]

#Valor inicial
p0 = dados_populacao_Brasil[0]

# Parâmetros p/ o Modelo de Verhulst
_pInfinito= 300000000
_r = 0.06

#Escolhendo os chutes iniciais para ajustar o modelo
chutes = [_pInfinito, _r]

#Ajusta os parâmetros
parametrosAjustados = leastsq(residual, chutes) # a saida desta função é do tipo [[x,y],z]

#Parâmetros Ajustados
pInfinito_Ajustado = parametrosAjustados[0][0]
r_Ajustado = parametrosAjustados[0][1]

print("\nParâmetros Ajustados")

#Trocando ',' por '.' e vice-versa
print("P∞: {0:,}".format(pInfinito_Ajustado).replace(',','*').replace('.',',').replace('*','.'))
print("r: {0:,}".format(r_Ajustado).replace(',','*').replace('.',',').replace('*','.'))


#Aplicando o modelo com os parâmetros ajustados
estimativa = odeint(modelo_gompertz, p0, dados_anos_censo, args=(pInfinito_Ajustado, r_Ajustado)) #Resolve o modelo com os parâmetros ajustados

#----------------Parte gráfica----------------
plt.plot(dados_anos_censo,dados_populacao_Brasil,'bo',label="Dados Experimentais") # Gráfico dos valores coletados
plt.plot(dados_anos_censo,estimativa,'g-',label="Curva ajustada:\nr: {0:,}".format(r_Ajustado).replace(',','*').replace('.',',').replace('*','.') + ", P∞: {0:,}".format(pInfinito_Ajustado).replace(',','*').replace('.',',').replace('*','.')) # Modelo Ajustado

#Calcula o erro absoluto
erroAbsoluto = abs(dados_populacao_Brasil - estimativa.T[0]) / dados_populacao_Brasil

print("\nMaior erro: {:.3}".format(max(erroAbsoluto)).replace(',','*').replace('.',',').replace('*','.'))
print("\nAcumulo de erro(soma dos erros absolutos): {:.3}".format(sum(erroAbsoluto)).replace(',','*').replace('.',',').replace('*','.'))

#Inserir legenda
plt.xlabel("Tempo (anos)\nTime (Years)")
plt.ylabel("População\nPopulation")
plt.title("Demografia do Brasil (Modelo de Gompertz)\n("+str(dados_anos_censo[0])+"-"+str(dados_anos_censo[len(dados_anos_censo)-1])+")"+"\nFonte: IBGE")
plt.legend()

#Exibir a interface
plt.show()