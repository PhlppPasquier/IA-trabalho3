import numpy as np


def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    accumulated_error = 0 # Cria uma variavel para guardar a soma dos erros
    for size, price in data: # Dado cada tamanho de propriedade e preço no banco de dados
        error = (price - (theta_0 + theta_1*size))  # Determina o erro
        accumulated_error += error*error/len(data)  # Soma o erro ao acumulador
    return accumulated_error # Retorna o erro somado


def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    accumulated_error0 = 0  # Cria variaveis para guardar a soma dos erros usada para calcular o gradiente
    accumulated_error1 = 0

    for size, price in data:
        error = (theta_0 + theta_1 * size - price)/len(data) # Calcula o erro produzido pelos thetas atuais (e ja divide pelo tamanho da base de dados para que o resultado não seja um número muito grande)
        accumulated_error0 += error  # Pega parte do valor do gradiente de theta 0
        accumulated_error1 += error*size  # Pega parte do valor do gradiente de theta 1

    new_theta_0 = theta_0 - alpha*2*accumulated_error0  # Calcula o novo valor de theta 0 a partir do seu gradiente
    new_theta_1 = theta_1 - alpha*2*accumulated_error1  # Calcula o novo valor de theta 1 a partir do seu gradiente

    return new_theta_0, new_theta_1  # Devolve os novos valores de theta 0 e 1


def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """
    theta_0_list = [theta_0] # Cria a lista de valores de theta 0
    theta_1_list = [theta_1] # Cria a lista de valores de theta 1

    for iteration in range(num_iterations): # Progride uma iteração até alcançar o numero de iterações pedido

        theta_0, theta_1 = step_gradient(theta_0, theta_1, data, alpha)  # Executa a descida de gradiente e salva os novos valores de theta 0 e 1

        theta_0_list.append(theta_0)  # Coloca o novo valor de theta 0 na lista
        theta_1_list.append(theta_1)  # Coloca o novo valor de theta 1 na lista

    return theta_0_list, theta_1_list  # Retorna as duas listas

if __name__ == '__main__':
    data = np.genfromtxt('alegrete.csv', delimiter=',')
    fit(data, -3, 6, 0.01, 90)
    '''
    Melhor solução:
    
    theta_0 = -3
    theta_1 = 6
    alpha = 0.01
    interactions = 90
    fit(data,-3,6,0.01,90)
    
    finishing thetas:
    -3.471544264398201, 1.1627591930896441
    '''
