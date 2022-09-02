from heapq import nsmallest
from random import randint, random, sample
import pandas as pd
import matplotlib.pyplot as plt


def evaluate(individual: list) -> int:
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 9.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    attacksCount = 0
    for i in range(7):
        for j in range(i + 1, 8):
            rowAttack = individual[i] == individual[j]
            diagonalAttack = (individual[i] - i == individual[j] - j 
                           or individual[i] + i == individual[j] + j)
            if rowAttack or diagonalAttack: 
                attacksCount += 1
    return attacksCount


def tournament(participants: list) -> list:
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    evalPopulation = [(p, evaluate(p)) for p in participants]
    bestIndividual, bestValue = min(evalPopulation, key=lambda x:x[1])
    return bestIndividual


def crossover(parent1: list, parent2: list, index: int) -> (list, list):
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
    offspring1 = parent1[:index] + parent2[index:]
    offspring2 = parent2[:index] + parent1[index:]
    return offspring1, offspring2
            

def mutate(individual: list, m: int) -> list:
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    newIndividual = individual.copy()
    if random() < m: 
        while newIndividual == individual:
            newIndividual[randint(0, 7)] = randint(1, 8)
    return newIndividual

def elitism(population: list, e: int) -> list:
    """
    Recebe uma população de individuos e retorna uma lista com 
    os n melhores elementos.
    :param population: list
    :param n: int - quantidade maxima da lista resultante
    :return: list - melhores indíviduos da população
    """
    evalPopulation = [(p, evaluate(p)) for p in population]
    evalPopulation.sort(key=lambda x:x[1])
    nSmallest = [evalPopulation[i][0] for i in range(e)]
    return nSmallest


def generate_random_population(size: int) -> list:
    """
    Dado um inteiro, retorna uma lista de Individuos aleatorios
    :param size: int - numero de individuos gerados
    :return: list - listas com os individuos
    """
    return [[randint(1, 8) for _ in range(8)] for _ in range(size)]


def evaluate_generation(population: list) -> dict:
    """
    Dado uma populacao, retorna o valor do melhor, do pior e da 
    média dos conflitos.
    :param population: list
    """
    evalPopulation = [evaluate(p) for p in population]
    return {
        'Min': min(evalPopulation),
        'Max': max(evalPopulation),
        'Average': sum(evalPopulation) / float(len(evalPopulation)),
    }


def plot_evolution(evolution: list):
    """
    Dado uma lista de evolucao, salva o grafico em um arquivo png
    :param evolution: list
    """
    df = pd.DataFrame(evolution)
    df = df[['Min', 'Max', 'Average']]
    ax = plt.gca()
    df.plot(kind='line',y='Min', color='blue', ax=ax)
    df.plot(kind='line',y='Max', color='red', ax=ax)
    df.plot(kind='line',y='Average', color='green', ax=ax)
    plt.ylim(ymin=0)  
    plt.xlim(xmin=0)
    plt.ylabel("Nº de ataques entre rainhas")
    plt.xlabel("Geração")
    plt.savefig("ga.png")


def run_ga(g: int, n: int, k: int, m: float, e: int) -> list:
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    population = generate_random_population(n)
    evolution = [evaluate_generation(population)]
    for generation in range(g):
        newPopulation = elitism(population, e)
        while len(newPopulation) < n:
            individual1 = tournament(sample(population, k))
            individual2 = tournament(sample(population, k))
            individual1, individual2 =  crossover(individual1, individual2, randint(0, 7))
            individual1 = mutate(individual1, m)
            individual2 = mutate(individual2, m)
            newPopulation.extend([individual1, individual2])
        evolution.append(evaluate_generation(newPopulation))
        population = newPopulation
    plot_evolution(evolution)
    return tournament(population)


run_ga(80, 20, 10, 0.6, 1)