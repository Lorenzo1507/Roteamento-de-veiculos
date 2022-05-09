import random
import math
import time
import copy
import numpy as np
'''### Introdução Teórica

Este problema é um caso especial do problema do Caixeiro-Viajante que é chamado do Problema de Roteamento de Veículos ou Vehicle Routing Problem (VRP). 

Este é um problema clássico para entregas em que vários veículos precisam fazer entregas ou captações em pontos específicos e precisam fazer a menor rota possível, evitar que rotas se sobreponham e saiam e voltem de depósitos.'''


'''Para o nosso problema, vamos considerar o número de vans variáveis, mas podemos testar com 4 vans.

### Os dados disponíveis

Neste problema, temos uma sequência de locais que podemos chamar de 0, 1, 2, 3, 4, ..., até N. O Local 0 (zero) é o local da padaria de onde as vans saem e chegam. 

Para a modelagem, iremos passar as distâncias entre os locais de pontos, por exemplo: entre 0 e 1, temos distância de 548.

Utilizar a seguinte matriz de distâncias:
https://replit.com/@celsosenac/ep-geneticos#main.py'''

'''### A modelagem

Devemos modelar um algoritmo genético que dada uma quantidade de N de vans e as distâncias entre os pontos de entrega, deve gerar:

- Genes e indivíduos: o que é um indivíduo neste problema
- Função de fitness: como saber a qualidade de um conjunto de rotas
- Função de mutação: como mudar a ordem das cidades e entre as vans
- Função de crossover: como trocar genes entre os indivíduos

Além disto, será necessário testar taxas de mutação, crossover e quantidade de indivíduos que sobrará em cada geração.

Exemplo de implementação:
https://replit.com/@celsosenac/aula05-geneticos'''


'''### A saída esperada

Para o número N de vans deve reproduzir a rota esperava de cada uma

Van 1:

2 → 5 → 3

Van 2: 

4 → 6 → 1'''


####################################################################################

#populacao é o conjunto de caminhos criados (cada caminho é um indivíduo)
def fitness(populacao):
  score = 0
  for i in range(len(melhor_caminho)):
    tupla = []
    tupla.append(melhor_caminho[i])
    
    tupla_p = populacao
    for j in tupla:
      if tupla == tupla_p: score += 1
  return score

def gerar_individuo():
  caminho = []
  for i in range(len(melhor_caminho)):
    caminho.append(random.choice(arcos))
  return caminho

def mutacao_flip(individuo):
  novo_individuo = individuo
  index = random.randint(0, 10 - 1)
  novo_individuo[index] = random.choice(lista_de_lugares) # mutando gene
  return [].append(novo_individuo)
  
# retorna populuacao mutada com uma taxa
def mutacao(populacao):
  populacao_escolhida = random.choices(populacao, k=math.ceil(tx_mutacao*len(populacao)))
  return [mutacao_flip(individuo) for individuo in populacao_escolhida]

def crossover(populacao, geracao):
  funcao_decaimento_crossover = 1 #math.exp(-geracao/200)
  qtd = funcao_decaimento_crossover*tx_crossover*len(populacao)
  populacao_crossover = []
  populacao_escolhida = random.choices(populacao, k=math.ceil(qtd))
  [1, 2, 3, 4]
  for i in range(len(populacao_escolhida) - 1):
    for j in range(i+1, len(populacao_escolhida)):
      ind1 = populacao_escolhida[i]
      ind2 = populacao_escolhida[j]

      index = random.randint(0, len(lista_de_lugares) - 1)
      populacao_crossover.append(ind1[0:index] + ind2[index:])
      populacao_crossover.append(ind2[0:index] + ind1[index:])

  return populacao_crossover

def selecao_com_tragedia(populacao, geracao):
  nova_populacao = sorted(populacao, key=fitness, reverse=True)
  if (geracao % geracoes_tragedia == 0):
    tamanho_tragedia = math.ceil(tamanho_populacao*tx_tragedia)
    novos_individuos = [gerar_individuo() for _ in range(0, tamanho_populacao - tamanho_tragedia)]
    return nova_populacao[0:tamanho_tragedia] + novos_individuos
  else:
    return nova_populacao[0:tamanho_populacao]


def selecao(populacao, geracao):
  nova_populacao = sorted(populacao, key=fitness, reverse=True)
  return nova_populacao[0:tamanho_populacao]


rnd = np.random
rnd.seed(0)

# variaveis globais
n = 10
vans = 4
clientes = [i for i in range(1, n+1)]

lista_de_lugares = [0] + clientes

#domínio
arcos = [(i,j) for i in lista_de_lugares for j in lista_de_lugares if i!=j]

#fim. baseado no menor custo e nas cidades que não passaram nenhuma vez (exceto pelo zero)
melhor_caminho = [(0,1), (1,10), (10,2), (2,6), (6,9), (9,4), (4,3), (3,5), (5,7), (7,8), (8,0)]

xc = rnd.rand(n+1)*200
yc = rnd.rand(n+1)*100

#custo
custo = {(i,j): np.hypot(xc[i]-xc[j], yc[i]-yc[j]) for i,j in arcos}

print("lugares: ", lista_de_lugares)
print("arcos: ", arcos)
print("custo: ", custo)

lista_global_deVans= [i for i in range(1, vans+1)]
tamanho_melhorCaminho = 0

#conjunto de indivíduos
tamanho_populacao = 3
tx_mutacao = 0.50
tx_crossover = 0.15
tx_tragedia = 0.05
geracoes_max = 100_000
geracoes_tragedia = 100

#10 cidades
gens = 10

    
#MAIN
#cria um vetor de 100 individuos, e cada indivíduo é um vetor com tupla
populacao = [gerar_individuo() for _ in range(0, tamanho_populacao)]
# ordernar lista
populacao = sorted(populacao, key=fitness, reverse=True)
geracao = 0

while fitness(populacao[0]) != len(lista_de_lugares) and geracao < geracoes_max:
  geracao += 1
  populacao_mutada = mutacao(populacao)
  populacao_crossover = crossover(populacao, geracao)
  populacao = selecao(populacao_mutada + populacao + populacao_crossover, geracao)
  
  if geracao % 100 == 0 or (geracao % 10 == 0 and geracao < 100):
    print("---------------- Intermediário: " + str(geracao)+ " ----------------")
    print("caminho: " + populacao[0])
    print("Tx Acerto: " + str(fitness(populacao[0])))

print("---------------- Final " + str(geracao) + " ----------------")
print("caminho: " + populacao[0])
print("Tx Acerto: " + str(fitness(populacao[0])))



  
