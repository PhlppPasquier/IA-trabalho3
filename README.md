# Trabalho Prático 3 - Otimização

## Alunos
* 00302213 - Filipe Ilunga Xindanhi (turma A)
* 00326970 - Henrique Borges Manzke (turma A)
* 00302923 - Philippe Silva Pasquier (turma A)

## Genética da Realeza
Parâmetros escolhidos: `g`: 80, `n`: 20, `k`: 10, `m`: 0.6, `e`: 1
![Screenshot](ga.png)\
Para executar o algoritmo genético com o gráfico da evolução do algoritmo, duas modificações devem ser feitas no arquivo eight_queens.py
- Primeiro: Descomentar a linha 150, que plota o gráfico da execução atual do ga
- Segundo: Descomentar a linha 154, que faz a chamada do ga com os parâmetros anteriores.

Obs.: Como o crossover e a mutação possuem randomicidade, os gráficos gerados em cada execução serão diferentes.

## Não me perguntes onde fica o Alegrete...

Valores iniciais inteiros que resultam na melhor execução da nossa regressão linear:

theta_0 = -3

theta_1 = 6

alpha = 0.01

num_iterations = 90


Valores finais aproximados:

theta_0 = -3.4650596837677825

theta_1 = 1.1621159649377641


O melhor erro quadrático médio obtido foi entorno de 8.527791858640681
(Que pode ser diminuido com um numero maior de iterações, porém, será uma melhoria imperceptivel)

