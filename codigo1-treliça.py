# Importando pandas para criar e manipular tabelas com informações importantes sobre o exercício
import pandas as pd

# Importando SymPy para manipulação de matrizes e vetores, bem como possibilitar matemática simbólica
import sympy as sp

# Tabela com dados importantes do exercício, como número de barras, ângulo de inclinação, comprimento, graus de liberdade,
# módulo de elasticidade do material e área da seção transversal

dados = {'Barra': ['(1)', '(2)', '(3)', '(4)', '(5)'],
         'teta': [16.7, -16.7, 135, 45, 90],
         'L (mm)': [1040, 1040, 1410, 1410, 700],
         'GDL 1': [1,3,5,1,3],
         'GDL 2': [2,4,6,2,4],
         'GDL 3': [3,5,7,7,7],
         'GDL 4': [4,6,8,8,8],
         'E': [200000,200000,200000,200000,200000],
         'A': [25,25,25,25,25]}

# Definindo símbolos dos deslocamentos/graus de liberdade e forças externas atuantes nos nós
q1,q2,q3,q4,q5,q6,q7,q8 = sp.symbols(['q1','q2','q3','q4','q5','q6','q7','q8'])
F1,F2,F3,F4,F5,F6,F7,F8 = sp.symbols(['F1','F2','F3','F4','F5','F6','F7','F8'])

dados_2 = {'u': [0,0,q3,q4,q5,0,q7,q8],
           'F': [F1,F2,0,0,0,F6,-20000,10000]}

# Criando o DataFrame (Tabela)
df = pd.DataFrame(dados)

# Criando tabelinha com condições de contorno
cc = pd.DataFrame(dados_2)

# Definindo símbolos de constantes e geometria relacionados à treliça
A, E, L, theta = sp.symbols(['A','E','L', 'theta'])

# Definindo c e s como cosseno de theta e seno de theta, respectivamente
c = sp.cos(theta)
s = sp.sin(theta)

# Definindo matriz de transformação para treliças (não consideramos rotações)
T = sp.Matrix([[c,s,0,0],[0,0,c,s]])

# Definindo matriz de rigidez local para cada elemento
Ke_local = sp.Matrix([[E*A/L,-E*A/L],[-E*A/L,E*A/L]])

# Definindo como calcular a matriz de rigidez global para cada elemento
Ke_global = T.T*Ke_local*T

# Criando função que recebe informações do elemento de treliça e faz a conversão para matriz de rigidez em coordenadas globais
def ROD(E_input,A_input,L_input,theta_input):
    # Conversão de theta para radianos
    theta_input = theta_input * 3.1415/180
    # Substituindo valores definidos na barra para a transformação
    Ke_g = Ke_global.subs(E,E_input).subs(A,A_input).subs(L,L_input).subs(theta,theta_input)
    # Retorna a matriz de rigidez global do elemento
    return Ke_g

# Criação da lista vazia que vai ser preenchida com a matriz global de todos os elementos de treliça
Lista_Ke_global = []

# Estrutura de repetição que aplica a função ROD para cada elemento de treliça e adiciona na lista de Ke's globais
for i in range(df.shape[0]):
    Lista_Ke_global.append(ROD(df['E'][i],df['A'][i],df['L (mm)'][i],df['teta'][i]))

# Define o número de graus de liberdade como sendo o valor máximo que aparece nas 4 colunas de graus de liberdade
N_GDL = int(df[['GDL 1','GDL 2','GDL 3','GDL 4']].values.max())

# Cria a matriz global de rigidez geral de zeros para ser preenchida, o tamanho é N_GDL x N_GDL
K = sp.Matrix.zeros(N_GDL)

# Estrutura para preencher a matriz global de rigidez geral
for n, row in df.iterrows(): # Faz uma iteração para cada linha da tabela como sendo uma lista
    GDL = [] # Lista vazia para preencher com os graus de liberdade relacionados na iteração
    GDL = row.iloc[3:7].tolist() # Preenchendo lista de graus de liberdade
    GDL = [x - 1 for x in GDL] # Substraindo 1 de cada grau de liberdade, necessário pela indexação do Python começar em 0

    # Iteração com as linhas da matriz de rigidez global da barra em questão
    for i in range(len(GDL)):
        # Iteração com as colunas da matriz de rigidez global da barra em questão
        for j in range(len(GDL)):
            K[GDL[i],GDL[j]] += Lista_Ke_global[n][i,j] # Preenchimento da matriz de rigidez global geral

# Transformando em vetores as informações de condições de contorno da tabela e as incógnitas a serem descobertas
F = sp.Matrix(cc.iloc[:, 1].tolist())
u = sp.Matrix(cc.iloc[:, 0].tolist())

# Montando o sistema linear
sistema = K * u - F

# Resolvendo o sistema linear
resultados = sp.solve(sistema, (F1,F2,q3,q4,q5,F6,q7,q8))
sp.pprint(resultados)
