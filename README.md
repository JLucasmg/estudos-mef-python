## _Estudos de Método dos Elementos Finitos (MEF) Python_

Repositório para documentar meus aprendizados no Método dos Elementos Finitos (MEF), com foco em aplicações estruturais utilizando Python.

### _Primeiro código:_

**Bibliotecas utilizadas: Pandas e SymPy**

Leitura de tabelas com parâmetros de treliças 2D para obter resultados de forças de reação e deslocamentos nodais. As tabelas devem conter informações como número do elemento de treliça (barra). Lembrando: contamos apenas com forças axiais no caso estudado.

**Estrutura das tabelas:**

A primeira tabela deve contar com uma coluna de barras, ângulo theta com relação ao eixo x, comprimento da barra em milímetros, enumeração dos 4 graus de liberdade de cada barra (em 4 colunas diferentes, uma para cada um da barra), módulo de elasticidade do material em MPa e área da seção transversal em mm². A segunda tabela é a de definição de condições de contorno, seu tamanho vai depender do número de barras/graus de liberdade no sistema de treliças inteiro, primeira coluna de deslocamento nodal (u) e segunda de forças nos nós (F).

### _Segundo código:_

**Bibliotecas utilizadas: Pandas e SymPy**

Leitura de tabelas com parâmetros de vigas 2D para obter resultados de forças de reação e deslocamentos nodais. As tabelas devem conter informações como número do elemento de viga. Lembrando: contamos com forças axiais, cortantes e momentos no caso estudado. Os primeiros elementos de cada nó são horizontais, os segundos são verticais e os terceiros são informações de momento.

**Estrutura das tabelas:**

A primeira tabela deve contar com uma coluna de vigas, ângulo theta com relação ao eixo x, comprimento da barra em milímetros, enumeração dos 6 graus de liberdade de cada barra (em 6 colunas diferentes, uma para cada um da viga), módulo de elasticidade do material em MPa, área da seção transversal em mm² e momento de inércia (I) em mm^4. A segunda tabela é a de definição de condições de contorno, seu tamanho vai depender do número de barras/graus de liberdade no sistema de treliças inteiro, primeira coluna de deslocamento nodal (u) e segunda de forças nos nós (F).
