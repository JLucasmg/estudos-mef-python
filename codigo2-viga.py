# Importando biblioteca Pandas
import pandas as pd

# Importando biblioteca SymPy
import sympy as sp

# Definindo dicionário de dados para o DataFrame com informações das vigas
dados = {'Barra': ['(1)','(2)'],
         'theta': [90,- 45],
         'L (mm)': [1000,1414.2],
         'GDL 1': [1,4],
         'GDL 2': [2,5],
         'GDL 3': [3,6],
         'GDL 4': [4,7],
         'GDL 5': [5,8],
         'GDL 6': [6,9],
        'E (MPa)': [80e3,80e3],
        'A (mm²)': [100, 100],
        'I': [10*10**3/12,10*10**3/12]}

# Definindo DataFrame com informações das vigas
df = pd.DataFrame(dados)

# Definindo símbolos dos nós e das forças e momentos envolvidos
q1,q2,q3,q4,q5,q6,q7,q8,q9 = sp.symbols(['q1','q2','q3','q4','q5','q6','q7','q8','q9'])
F1,F2,F3,F4,F5,F6,F7,F8,F9 = sp.symbols(['F1','F2','F3','F4','F5','F6','F7','F8','F9'])

# Definição do dicionário de informações para o DataFrame de condições de contorno
dados_2 = {'u': [0,0,0,q4,q5,q6,0,0,0],
           'F': [F1,F2,F3,-10e3,-0,0,F7,F8,F9]}

# Definição do DataFrame de condições de contorno
cc = pd.DataFrame(dados_2)

# Definição de símbolos de constantes utilizadas
A,E,L,I,theta = sp.symbols(['A','E','L','I','theta'])

# Definindo c como cosseno de theta e s como seno de theta
c = sp.cos(theta)
s = sp.sin(theta)

# Definição da matriz de rigidez em coordenadas locais do elemento de viga
Ke_local = sp.Matrix([[E*A/L,0,0,-E*A/L,0,0],
                  [0,12*E*I/L**3,6*E*I/L**2,0,-12*E*I/L**3,6*E*I/L**2],
                  [0,6*E*I/L**2,4*E*I/L,0,-6*E*I/L**2,2*E*I/L],
                  [-E*A/L,0,0,E*A/L,0,0],
                  [0,-12*E*I/L**3,-6*E*I/L**2,0,12*E*I/L**3,-6*E*I/L**2],
                  [0,6*E*I/L**2,2*E*I/L,0,-6*E*I/L**2,4*E*I/L]])

# Definindo matriz de transformação
T = sp.Matrix([[c,-s,0,0,0,0],
               [s,c,0,0,0,0],
               [0,0,1,0,0,0],
               [0,0,0,c,-s,0],
               [0,0,0,s,c,0],
               [0,0,0,0,0,1]]).T

# Definindo fórmula para o cálculo da matriz de rigidez em coordenadas globais do elemento de viga
Ke_global = T.T*Ke_local*T

# Definindo função que retorna a matriz de rigidez em coordenadas globais do elemento com inputs de informação da viga
def beam(I_input,E_input,A_input,L_input,theta_input):
    # Conversão de theta para radianos
    theta_input = theta_input * 3.1415/180
    # Substituindo valores definidos na barra para a transformação
    Ke_g = Ke_global.subs(E,E_input).subs(A,A_input).subs(L,L_input).subs(I,I_input).subs(theta,theta_input)
    # Retorna a matriz de rigidez global do elemento
    return Ke_g

# Criando lista de todas as matrizes de rigidez em coordenadas globais dos elementos de viga
Lista_Ke_global = []

# Aplicando função beam em todos os elementos de viga do DataFrame
for i in range(df.shape[0]):
    Lista_Ke_global.append(beam(df['I'][i],df['E (MPa)'][i],df['A (mm²)'][i],df['L (mm)'][i],df['theta'][i]))

# Definindo número máximo de graus de liberdade
N_GDL = int(df[['GDL 1','GDL 2','GDL 3','GDL 4','GDL 5','GDL 6']].values.max())

# Criando matriz de zeros para preenchimento da Matriz de Rigidez Global.
K = sp.Matrix.zeros(N_GDL)

# Estrutura para preencher a matriz global de rigidez geral
for n, row in df.iterrows(): # Faz uma iteração para cada linha da tabela como sendo uma lista
    GDL = [] # Lista vazia para preencher com os graus de liberdade relacionados na iteração
    GDL = row.iloc[3:9].tolist() # Preenchendo lista de graus de liberdade
    GDL = [x - 1 for x in GDL] # Substraindo 1 de cada grau de liberdade, necessário pela indexação do Python começar em 0

    # Iteração com as linhas da matriz de rigidez global da barra em questão
    for i in range(len(GDL)):
        # Iteração com as colunas da matriz de rigidez global da barra em questão
        for j in range(len(GDL)):
            K[GDL[i],GDL[j]] += Lista_Ke_global[n][i,j] # Preenchimento da matriz de rigidez global geral

# Definindo vetores de força e deslocamento nodal para a resolução do sistema linear
F = sp.Matrix(cc.iloc[:, 1].tolist())
u = sp.Matrix(cc.iloc[:, 0].tolist())

# Resolução do sistema linear, obtenção das forças de reação e deslocamentos nodais
sistema = K * u - F
sp.linsolve(sistema,(F1,F2,F3,q4,q5,q6,F7,F8,F9))
