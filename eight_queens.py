from random import randint, random, sample
from matplotlib.pyplot import gca, savefig, ylim, xlim
from pandas import DataFrame

def evaluate(individual: list) -> int:
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    attacks = 0
    for i in range(7):
        for j in range(i+1, 8):
            columnsAttack = individual[i] == individual[j]
            diagonalAttack = individual[i] - i == individual[j] - j or individual[i] + i == individual[j] + j
            if columnsAttack or diagonalAttack: attacks += 1
    return attacks


def tournament(participants: list) -> list:
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    return min([(evaluate(p), p) for p in participants], key=lambda x:x[0])[1]


def crossover(parent1: list, parent2: list, index: int) -> tuple[list, list]:
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    return (parent1[:index] + parent2[index:], 
            parent2[:index] + parent1[index:])


def mutate(individual: list, m: int):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    if random() < m: 
        individual[randint(0, 7)] = randint(1, 8)
    return individual

def generate_random_population(size: int) -> list:
    return [[randint(1, 8) for _ in range(8)] for _ in range(size)]

def evaluate_population(population: list) -> dict:
    evaluatePopulation = [evaluate(p) for p in population]
    return {
        'min': min(evaluatePopulation),
        'max': max(evaluatePopulation),
        'mean': sum(evaluatePopulation) / float(len(evaluatePopulation)),
    }

def plot_evolution(evolution: list):
    df = DataFrame(evolution)
    df = df[['min', 'max', 'mean']]
    ax = gca()
    df.plot(kind='line',y='min', color='blue', ax=ax)
    df.plot(kind='line',y='max', color='red', ax=ax)
    df.plot(kind='line',y='mean', color='green', ax=ax)
    ylim(ymin=0)  # this line
    xlim(xmin=0)  # this line
    savefig("ga.png")

def run_ga(g: int, n: int, k: int, m: float, e: bool, plot=False) -> list:
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    Plota o grafico da evolucao da populacao.
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:bool - se vai haver elitismo
    :return:list - melhor individuo encontrado
    """     
    evolution = []
    population = generate_random_population(n)
    for generation in range(g):
        newPopulation = [tournament(population)] if e else [] 
        while len(newPopulation) < n:
            individual1 = tournament(sample(population, k))
            individual2 = tournament(sample(population, k))
            individual1, individual2 =  crossover(individual1, individual2, 4)
            individual1 = mutate(individual1, m)
            individual2 = mutate(individual2, m)
            newPopulation.extend([individual1, individual2])
        evolution.append(evaluate_population(newPopulation))
        population = newPopulation
    if plot: plot_evolution(evolution)
    return tournament(population)

run_ga(80, 20, 10, 0.6, True, True)