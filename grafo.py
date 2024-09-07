from collections import defaultdict, deque
import sys
import heapq

class Grafo:
    def __init__(self):
        """
        Inicializa um grafo com as estruturas necessárias para armazenar os vértices,
        arestas e pesos. Também chama uma função que armazena o grafo em uma estrutura de dados.

        Atributos:
            grafo (dict): Representação do grafo onde as chaves são os vértices e os valores
                          são os vértices adjacentes com seus respectivos pesos.
            qtdVertices (int): A quantidade de vértices no grafo.
            visitado (list): Lista de vértices visitados para algoritmos de busca.
            matriz_adjacencia (list): Matriz de adjacência para representar as arestas do grafo.
        """
        # self.grafo = {}
        self.grafo = defaultdict(dict)
        self.qtdVertices = 0
        self.visitado = []
        self.lista_adjacencia = {}
        self.matriz_adjacencia = []
        self.armazenar_grafo()

    def armazenar_grafo(self):
        """
        Lê o arquivo de entrada e armazena o grafo.

        O arquivo de entrada deve conter a quantidade de vértices na primeira linha e,
        nas linhas subsequentes, as arestas entre dois vértices, seguidas pelo peso 
        (se o grafo for ponderado).

        Formato esperado do arquivo:
        - Primeira linha: número de vértices (inteiro).
        - Linhas seguintes: vértice1 vértice2 [peso], onde 'peso' é opcional.

        O grafo será armazenado tanto como uma matriz de adjacência quanto como um dicionário 
        de listas de adjacência.

        """

        with open('entrada.txt', 'r') as arquivo:
            # Lê a primeira linha separadamente
            self.qtdVertices = int(next(arquivo).strip())
            self.matriz_adjacencia = [[0 for _ in range(self.qtdVertices)] for _ in range(self.qtdVertices)]

            for linha in arquivo:
                numeros = linha.split()
                if len(numeros) >= 3:
                    vertice1 = int(numeros[0])
                    vertice2 = int(numeros[1])
                    peso = float(numeros[2])
                    
                    self.grafo[vertice1][vertice2] = peso
                    self.grafo[vertice2][vertice1] = peso
                    self.matriz_adjacencia[vertice1-1][vertice2-1] = peso
                    self.matriz_adjacencia[vertice2-1][vertice1-1] = peso
                elif len(numeros) == 2:
                    vertice1 = int(numeros[0])
                    vertice2 = int(numeros[1])

                    self.grafo[vertice1][vertice2] = 1
                    self.grafo[vertice2][vertice1] = 1
                    self.matriz_adjacencia[vertice1-1][vertice2-1] = 1
                    self.matriz_adjacencia[vertice2-1][vertice1-1] = 1

        # print(self.grafo)

    def informacoes(self):
        """
        Gera informações sobre o grafo, como a quantidade de vértices, arestas e grau médio.

        A função lê o arquivo de entrada para contar o número de arestas e calcular o grau médio
        dos vértices. As informações são gravadas em um arquivo de saída ('saida.txt').

        O arquivo de saída incluirá:
        - A quantidade de vértices.
        - A quantidade de arestas.
        - O grau médio dos vértices.
        - A distribuição empírica dos graus dos vértices.
        """

        mensagem = ''
        contagem_arestas = 0
        soma_grau = 0

        with open('entrada.txt', 'r') as arquivo:
            # Lê a primeira linha separadamente
            qtdVertices = next(arquivo).strip()
            mensagem += f"Quantidade de vertices: {qtdVertices}\n"
            contagem_numeros = defaultdict(int)

            # Agora lê o restante das linhas
            for linha in arquivo:
                contagem_arestas+=1
                numeros = linha.split()

                if len(numeros) == 3:
                    for numero in numeros[:-1]:  # Ignora o último número
                        numero = int(numero)  # Converte para inteiro
                        contagem_numeros[numero] += 1  # Incrementa a contagem para esse número
                else:
                    for numero in numeros:
                        numero = int(numero)  # Converte para inteiro
                        contagem_numeros[numero] += 1  # Incrementa a contagem para esse número
                    
            mensagem += f"Quantidade de arestas: {contagem_arestas}\n"

            # Exibe o número de ocorrências de cada número
            for numero, contagem in contagem_numeros.items():
                # Incrementa a soma dos graus de cada vértice para se realizar o cálculo do grau médio posteriormente
                soma_grau += contagem
            
            mensagem += f"Grau medio: {int(soma_grau)/int(qtdVertices)}\n"

            # Resgata o maior valor registrado no dicionário (grau máximo)
            maior_grau = max(contagem_numeros.values())
        
            # Contagem de quantos vértices têm cada grau
            contagem_graus = defaultdict(int)
            for grau in contagem_numeros.values():
                contagem_graus[grau] += 1
            
            # DISTRIBUIÇÃO EMPÍRICA
            for grau in range(1, maior_grau + 1):
                qtd = contagem_graus.get(grau, 0) # Se o grau não existir, retorna 0
                mensagem += f'{grau} {int(qtd) / int(qtdVertices)}\n'
        
        with open('saida.txt', 'w') as arquivo_saida:
            arquivo_saida.write('--------------INFORMACOES DO GRAFO--------------\n\n')

        with open('saida.txt', 'a') as arquivo_saida:
            arquivo_saida.write(f'{mensagem}\n')
        
        return print('Arquivo de saida com informacoes gerado')
    
    def representacao(self):
        """
        Permite ao usuário escolher entre representar o grafo por matriz de adjacência ou lista de adjacência.

        A função interativa solicita ao usuário que escolha a forma de representação e chama a função
        correspondente para exibir a matriz ou lista de adjacência.
        """

        while True:
            print('Digite 1 para Representação por matriz de adjacência')
            print('Digite 2 para Representação por lista de adjacência')
            try:
                escolha = int(input("Escolha: "))
                
                if escolha == 1:
                    self.rep_matriz()
                    break  
                elif escolha == 2:
                    self.rep_lista()
                    break  
                else:
                    print("Opção inválida! Por favor, digite 1 ou 2.")
            except ValueError as e:
                print(f"Erro de valor: {e}")

    def rep_matriz(self):
        """
        Exibe a matriz de adjacência do grafo.

        A matriz de adjacência é impressa no console, mostrando as conexões entre os vértices.
        """
        print('==================== RESULTADO =========================\n')        
        return print(f'Matriz de adjacencia: \n\n{self.matriz_adjacencia}\n')
    
    def rep_lista(self):
        """
        Exibe a lista de adjacência do grafo.

        A função lê o arquivo de entrada novamente para construir e imprimir a lista de adjacência
        do grafo no console.
        """

        with open('entrada.txt', 'r') as arquivo:
            lista_adjacencia = ''

            # Lê a primeira linha separadamente
            qtdVertices = int(next(arquivo).strip())
            relacionamento_numeros = defaultdict(str)
            numeros_unicos = set()

            for linha in arquivo:
                numeros = linha.split()
                vertice1 = numeros[0]
                vertice2 = numeros[1]
                    
                relacionamento_numeros[f'{vertice1}'] += f'-> {vertice2}'
                relacionamento_numeros[f'{vertice2}'] += f'-> {vertice1}'

                if len(numeros) == 3:
                    for numero in numeros[:-1]:
                        numeros_unicos.add(int(numero)) 
                else:
                    for numero in numeros:
                        numeros_unicos.add(int(numero)) 

            for numero_unico in numeros_unicos:
                lista_adjacencia += f'{numero_unico}{relacionamento_numeros[f'{numero_unico}']}\n'

            print('\n')
            print('==================== RESULTADO =========================\n')
            
        return print(f'Lista de Adjacencia: \n\n{lista_adjacencia}')
    
    def _dfs_componente(self, v, visitado, componente_atual):
        """
        Realiza uma busca em profundidade (DFS) para encontrar componentes conexos.

        Este método é utilizado internamente para identificar todos os vértices em um componente conexo,
        partindo de um vértice específico.

        Parâmetros:
            v (int): O vértice atual.
            visitado (list): Lista que rastreia os vértices visitados.
            componente_atual (list): Lista de vértices que pertencem ao componente conexo atual.
        """

        visitado[v] = True
        componente_atual.append(v)
        
        for u in self.grafo[v]:
            if not visitado[u]:
                self._dfs_componente(u, visitado, componente_atual)

    def busca_profundidade(self, v, primeira_chamada=True, caminho=[], pai='Nenhum', nivel=0, saida=[]):
        """
        Realiza a busca em profundidade (DFS) a partir de um vértice.

        A função percorre o grafo utilizando DFS, rastreando o caminho, o nível e o pai de cada vértice.
        Os resultados são armazenados em uma lista e gravados em um arquivo de saída.

        Parâmetros:
            v (int): O vértice inicial para a DFS.
            primeira_chamada (bool): Indica se é a primeira chamada da função (padrão: True).
            caminho (list): Lista que armazena o caminho percorrido.
            pai (str): Pai do vértice atual na árvore de DFS (padrão: 'Nenhum').
            nivel (int): Nível do vértice atual na árvore de DFS (padrão: 0).
            saida (list): Lista que armazena as informações para o arquivo de saída.
        """

        if v in self.grafo.keys():

            if not self.visitado:
                self.visitado = [False] * (len(self.grafo) + 1)
            
            self.visitado[v] = True
            caminho.append(f' {v} ')  # Adiciona o vértice ao caminho
            saida.append(f'Vertice: {v} -> Nivel: {nivel} | Pai: {pai} \n')

            for u in self.grafo[v]:
                if not self.visitado[u]:
                    self.busca_profundidade(u, primeira_chamada=False, caminho=caminho, pai=str(v), nivel=nivel+1, saida=saida)

            if primeira_chamada:
                # Imprime o caminho ao final da pilha de execuções da chamada recursiva
                saida.append('\n')
                saida.append("->".join(map(str, caminho)))
                
                with open('saida.txt', 'a') as arquivo_saida:
                    arquivo_saida.write('--------------BUSCA POR PROFUNDIDADE--------------\n\n')
                    arquivo_saida.write(f'{"".join(saida)}\n\n')
                    return print('Arquivo de saida atualizado com informacoes da busca por profundidade')
        else:
            print('Não existe esse vértice no grafo, chame a função com outro vértice inicial')

    def busca_largura(self, v):
        """
        Realiza a busca em largura (BFS) a partir de um vértice.

        A função percorre o grafo utilizando BFS, rastreando o nível e o pai de cada vértice.
        Os resultados são armazenados em uma lista e gravados em um arquivo de saída.

        Parâmetros:
            v (int): O vértice inicial para a BFS.
        """

        if v in self.grafo.keys():

            visitadoLargura = [False] * (len(self.grafo) + 1)

            fila = deque([v])  # Usamos deque para operações eficientes de fila
            nivel = {v: 0}  # Dicionário para rastrear o nível de cada vértice
            pai = {v: 'Nenhum'} # Dicionário para rastrear o pai de cada vértice
            resultado = []

            while fila:
                vAtual = fila.popleft()  # Remove o primeiro elemento da fila
                if not visitadoLargura[vAtual]:
                    resultado.append(vAtual)
                    visitadoLargura[vAtual] = True
                    for i in self.grafo[vAtual]:
                        if not visitadoLargura[i]:
                            fila.append(i)
                            pai[i] = str(vAtual)
                            nivel[i] = nivel[vAtual] + 1
            
            with open('saida.txt', 'a') as arquivo_saida:
                saida = ''
                for vertice in resultado:
                    saida += (f"Vertice: {vertice} -> Nivel: {nivel[vertice]} | Pai: {pai[vertice]}\n")
                saida += f'\n'+ " -> ".join(map(str, resultado))
                arquivo_saida.write('--------------BUSCA POR LARGURA--------------\n\n')
                arquivo_saida.write(f'{saida}\n\n')
                return print('Arquivo de saida atualizado com informacoes da busca por largura')
        else:
            print('Não existe esse vértice no grafo, chame a função com outro vértice inicial')

    def encontrar_componentes_conexos(self):
        """
        Encontra e exibe os componentes conexos do grafo.

        A função identifica todos os componentes conexos no grafo, utilizando DFS.
        Cada componente é impresso com a lista de vértices que o compõem.

        """

        visitado = [False] * (len(self.grafo) + 1)
        componentes = []
        componentes_contagem = {}
        
        # Realiza a DFS para encontrar todos os componentes conexos
        for v in self.grafo:
            if not visitado[v]:
                componente_atual = []
                self._dfs_componente(v, visitado, componente_atual)
                componentes.append(componente_atual)
        
        print(f"\nNúmero de componentes conexos do grafo: {len(componentes)}")

        # Preenche o dicionário de contagem de componentes
        for i, componente in enumerate(componentes):
            tamanho_componente = len(componente)
            componentes_contagem[i + 1] = tamanho_componente  # Associa o componente ao seu tamanho

        # Imprime cada componente e seu respectivo tamanho
        for i, componente in enumerate(componentes):
            tamanho_componente = componentes_contagem[i + 1]
            print(f"Componente {i + 1} -> Lista de vértices: {componente} | Tamanho: {tamanho_componente}")
        
        print('')

    def tem_pesos_negativos(self):
        """
        Verifica se o grafo possui arestas com pesos negativos.

        Esta função é utilizada para determinar se o algoritmo de Dijkstra pode ser aplicado.

        Retorna:
            bool: True se houver pesos negativos, False caso contrário.
        """

        for u in self.grafo:
            for v in self.grafo[u]:
                if self.grafo[u][v] < 0:
                    return True
        return False

    def _calcular_bfs(self, origem, destino):
        visitado = {v: False for v in self.grafo}
        distancias = {v: sys.maxsize for v in self.grafo}
        antecessor = {v: None for v in self.grafo}

        fila = deque([origem])
        visitado[origem] = True
        distancias[origem] = 0

        while fila:
            u = fila.popleft()

            for v in self.grafo[u]:
                if not visitado[v]:
                    visitado[v] = True
                    distancias[v] = distancias[u] + 1
                    antecessor[v] = u
                    fila.append(v)
                    if v == destino:
                        break

        caminho = []
        atual = destino
        while atual is not None:
            caminho.insert(0, atual)
            atual = antecessor[atual]

        print(f"Caminho mínimo de {origem} para {destino} usando BFS: {caminho}")
        print(f"Distância: {distancias[destino]}")

        return caminho, distancias[destino]

    def _calcular_dijkstra(self, origem, destino):
        distancias = {v: sys.maxsize for v in self.grafo}
        distancias[origem] = 0
        antecessor = {v: None for v in self.grafo}
        pq = [(0, origem)]

        while pq:
            dist_u, u = heapq.heappop(pq)

            if dist_u > distancias[u]:
                continue

            for v in self.grafo[u]:
                peso = self.grafo[u][v]
                if distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    antecessor[v] = u
                    heapq.heappush(pq, (distancias[v], v))

        caminho = []
        atual = destino
        if distancias[destino] != sys.maxsize:
            while atual is not None:
                caminho.insert(0, atual)
                atual = antecessor[atual]
            print(f"Caminho mínimo de {origem} para {destino} usando Dijkstra: {caminho}")
            print(f"Distância: {distancias[destino]}")
        else:
            print(f"{destino} não é acessível a partir de {origem}")

    def _calcular_bfs_para_todos(self, origem):
        # Implementação de BFS para todos os vértices
        visitado = {v: False for v in self.grafo}
        distancias = {v: sys.maxsize for v in self.grafo}
        antecessor = {v: None for v in self.grafo}

        fila = deque([origem])
        visitado[origem] = True
        distancias[origem] = 0

        while fila:
            u = fila.popleft()

            for v in self.grafo[u]:
                if not visitado[v]:
                    visitado[v] = True
                    distancias[v] = distancias[u] + 1
                    antecessor[v] = u
                    fila.append(v)

        # Exibe as distâncias
        for destino in distancias:
            if distancias[destino] != sys.maxsize:
                caminho = []
                atual = destino
                while atual is not None:
                    caminho.insert(0, atual)
                    atual = antecessor[atual]

                print(f"Caminho mínimo de {origem} para {destino} usando BFS: {caminho}")
                print(f"Distância: {distancias[destino]}")
            else:
                print(f"{destino} não é acessível a partir de {origem}")

        return distancias

    def _calcular_dijkstra_para_todos(self, origem):
        distancias = {v: sys.maxsize for v in self.grafo}
        distancias[origem] = 0
        antecessor = {v: None for v in self.grafo}
        pq = [(0, origem)]

        while pq:
            dist_u, u = heapq.heappop(pq)

            if dist_u > distancias[u]:
                continue

            for v in self.grafo[u]:
                peso = self.grafo[u][v]
                if distancias[u] + peso < distancias[v]:
                    distancias[v] = distancias[u] + peso
                    antecessor[v] = u
                    heapq.heappush(pq, (distancias[v], v))

        # Exibe as distâncias
        for destino in distancias:
            if distancias[destino] != sys.maxsize:
                caminho = []
                atual = destino
                while atual is not None:
                    caminho.insert(0, atual)
                    atual = antecessor[atual]

                print(f"Caminho mínimo de {origem} para {destino} usando Dijkstra: {caminho}")
                print(f"Distância: {distancias[destino]}")
            else:
                print(f"{destino} não é acessível a partir de {origem}")

        return distancias

    def calcular_caminho_minimo(self, origem, destino=None):
        """
        Calcula o caminho mínimo em um grafo a partir de um vértice de origem.

        Dependendo dos parâmetros fornecidos, a função pode realizar dois tipos de cálculos:
        
        1. Se apenas o parâmetro `origem` for fornecido:
        - Calcula o caminho mínimo do vértice de origem para todos os outros vértices no grafo.
        - Se o grafo não tiver pesos ou se todos os pesos forem iguais a 1, utiliza o algoritmo de Busca em Largura (BFS).
        - Se o grafo tiver pesos positivos, utiliza o algoritmo de Dijkstra.

        2. Se os parâmetros `origem` e `destino` forem fornecidos:
        - Calcula o caminho mínimo entre o vértice de origem e o vértice de destino.
        - Se o grafo não tiver pesos ou se todos os pesos forem iguais a 1, utiliza o algoritmo de Busca em Largura (BFS).
        - Se o grafo tiver pesos positivos, utiliza o algoritmo de Dijkstra.

        Parâmetros:
        ----------
        origem : int
            O vértice de origem a partir do qual o caminho mínimo será calculado.
        
        destino : int, opcional
            O vértice de destino para o qual o caminho mínimo será calculado.
            Se não for fornecido, a função calcula o caminho mínimo do vértice de origem para todos os outros vértices.
        
        Retorna:
        --------
        Se `destino` for fornecido:
            tuple: Um par contendo o caminho mínimo como uma lista de vértices e a distância mínima entre `origem` e `destino`.
        
        Se `destino` não for fornecido:
            dict: Um dicionário onde as chaves são os vértices e os valores são as distâncias mínimas do vértice de origem para cada um dos outros vértices.
        
        Exceções:
        ---------
        Se o grafo contiver pesos negativos, a função imprime uma mensagem de erro e não realiza o cálculo, pois o algoritmo de Dijkstra não é adequado para grafos com pesos negativos.

        Exemplos de Uso:
        ----------------
        >>> grafo.calcular_caminho_minimo(1)
        Calcula o caminho mínimo do vértice 1 para todos os outros vértices.

        >>> grafo.calcular_caminho_minimo(1, 4)
        Calcula o caminho mínimo do vértice 1 para o vértice 4.

        """
        
        if destino is None:
            
            # Se apenas o parâmetro `origem` foi passado, calcular caminhos mínimos de `origem` para todos os vértices
            if self.tem_pesos_negativos():
                print("Erro: O grafo possui pesos, porém o algoritmo de Dijkstra não pode ser usado com pesos negativos.")
                return

            if all(peso == 1 for adj in self.grafo.values() for peso in adj.values()):
                # Se todos os pesos são 1, use BFS
                return self._calcular_bfs_para_todos(origem)
            else:
                # Caso contrário, use Dijkstra
                return self._calcular_dijkstra_para_todos(origem)
        else:
            
            # Se `origem` e `destino` foram passados, calcular caminho mínimo entre esses dois vértices
            if self.tem_pesos_negativos():
                print("Erro: O grafo possui pesos, porém o algoritmo de Dijkstra não pode ser usado com pesos negativos.")
                return

            if all(peso == 1 for adj in self.grafo.values() for peso in adj.values()):
                # Se todos os pesos são 1, use BFS
                return self._calcular_bfs(origem, destino)
            else:
                # Caso contrário, use Dijkstra
                return self._calcular_dijkstra(origem, destino)

def main():
   
    grafo = Grafo()

    # grafo.calcular_caminho_minimo(0)
    # grafo.calcular_caminho_minimo(1,4)
    # grafo.representacao()
    grafo.informacoes()
    # grafo.busca_profundidade(2)
    # grafo.busca_largura(1)
    grafo.encontrar_componentes_conexos()


if __name__ == "__main__":
    main()



# def desenhar_grafo(matriz_adjacencia):
#         qtdVertices = len(matriz_adjacencia)

#         # Para cada vértice, verificamos suas conexões
#         for i in range(qtdVertices):
#             for j in range(i, qtdVertices):
#                 if matriz_adjacencia[i][j] == 1:
#                     # Conexão horizontal
#                     print(f"{i+1} -- {j+1}")
        
#         print("\nRepresentação Completa do Grafo:")
#         for i in range(qtdVertices):
#             print(f"{i+1}: ", end="")
#             for j in range(qtdVertices):
#                 if matriz_adjacencia[i][j] == 1:
#                     print(f" {j+1}", end="")
#             print()


