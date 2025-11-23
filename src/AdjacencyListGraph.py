from src.AbstractGraph import AbstractGraph
import heapq
import math 

class AdjacencyListGraph(AbstractGraph):
    """
    Implementação utilizando Lista de Adjacência.
    Estrutura: Uma lista onde cada posição 'u' contém um dicionário
    {v: peso, v2: peso2}
    """


    def __init__(self, num_vertices): # [cite: 50]
        super().__init__(num_vertices)
        self.adj_list = [{} for _ in range(num_vertices)]
        self.num_edges = 0

    def get_edge_count(self):
        return self.num_edges

    def has_edge(self, u, v):
        self.validate_index(u)
        self.validate_index(v)
        return v in self.adj_list[u]

    def add_edge(self, u, v):
        self.validate_index(u)
        self.validate_index(v)
        
        if u == v: return # Sem laços
        
        if v not in self.adj_list[u]:
            self.adj_list[u][v] = 1.0 # Peso padrão
            self.num_edges += 1

    def remove_edge(self, u, v):
        if self.has_edge(u, v):
            del self.adj_list[u][v]
            self.num_edges -= 1

    def set_edge_weight(self, u, v, w):
        if self.has_edge(u, v):
            self.adj_list[u][v] = float(w)

    def get_edge_weight(self, u, v):
        if self.has_edge(u, v):
            return self.adj_list[u][v]
        return 0.0

    # --- Lógica de Grafos ---

    def is_successor(self, u, v):
        return self.has_edge(u, v)

    def is_predecessor(self, u, v):
        return self.has_edge(v, u)

    def is_divergent(self, u1, v1, u2, v2):
        if not (self.has_edge(u1, v1) and self.has_edge(u2, v2)):
            raise ValueError("Uma das arestas não existe.")
        return u1 == u2 and v1 != v2

    def is_convergent(self, u1, v1, u2, v2):
        if not (self.has_edge(u1, v1) and self.has_edge(u2, v2)):
            raise ValueError("Uma das arestas não existe.")
        return v1 == v2 and u1 != u2

    def is_incident(self, u, v, x):
        if not self.has_edge(u, v):
            return False
        return x == u or x == v

    def get_vertex_in_degree(self, u):
        self.validate_index(u)
        in_degree = 0
        for i in range(self.num_vertices):
            if u in self.adj_list[i]:
                in_degree += 1
        return in_degree

    def get_vertex_out_degree(self, u):
        self.validate_index(u)
        return len(self.adj_list[u])

    def is_empty_graph(self):
        return self.num_edges == 0

    def is_complete_graph(self):
        max_edges = self.num_vertices * (self.num_vertices - 1)
        return self.num_edges == max_edges

    def is_connected(self):
        if self.num_vertices == 0: return True
        
        # Cria uma versão "não direcionada" temporária apenas para checagem
        # Ou verifica conectividade fraca via BFS
        visited = [False] * self.num_vertices
        queue = [0]
        visited[0] = True
        count_visited = 0
        
        while queue:
            u = queue.pop(0)
            count_visited += 1
            
            # Vizinhos diretos (saída)
            neighbors = list(self.adj_list[u].keys())
            
            # Vizinhos inversos (entrada) - custoso em lista de adjacência, mas necessário para "weakly connected"
            for i in range(self.num_vertices):
                if u in self.adj_list[i]:
                    neighbors.append(i)
            
            for v in neighbors:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
                    
        return count_visited == self.num_vertices
        
    # --- Métricas de Grafos --- Analise do repositorio (Etapa 3)

    # --- Metricas de centralidade ---
    def get_normalized_degree_centrality(self, u):
        """
        calcula o grau centralizado normalizado do vértice u
        """
        self.validate_index(u)
        degree = self.get_vertex_in_degree(u) + self.get_vertex_out_degree(u)
        if self.num_vertices <= 1:
            return 0.0
        return degree / (self.num_vertices - 1)
    
    def dijkstra(self, start):
        """
        Implementa o algoritmo de Dijkstra para encontrar o caminho mais curto
        a partir do vértice 'start' para todos os outros vértices no grafo.
        Retorna um dicionário com as distâncias mínimas.
        """
        self.validate_index(start)
        distances = {v: float('inf') for v in range(self.num_vertices)}
        distances[start] = 0.0
        predecessors = {v: [] for v in range(self.num_vertices)}
        priority_queue = [(0.0, start)]  # (distância, vértice)

        # Contagem de caminhos mais curtos para o Betweenness Centrality
        shortest_path_count = {node: 0 for node in range(self.num_vertices)}
        shortest_path_count[start] = 1  # Há um caminho mais curto para o nó inicial
    

        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)

            if current_distance > distances[u]:
                continue

            for v, weight in self.adj_list[u].items():
                distance = current_distance + weight

                if distance < distances[v]:
                    distances[v] = distance
                    predecessors[v] = [u] # novo caminho mais curto
                    shortest_path_count[v] = shortest_path_count[u] # atualiza contagem de caminhos mais curtos
                    heapq.heappush(priority_queue, (distance, v))
                elif distance == distances[v]:
                    predecessors[v].append(u) # caminho alternativo
                    shortest_path_count[v] += shortest_path_count[u] # incrementa contagem de caminhos mais curtos

        return distances, predecessors, shortest_path_count
    
    def get_closeness_centrality(self, u):
        """
        Calcula a centralidade de proximidade do vértice u
        """
        self.validate_index(u)
        distances, _, _ = self.dijkstra(u)
        sum_distances = 0.0
        reachable_vertices = 0 # Vértices alcançáveis a partir de u excluindo ele mesmo
        for v in range(self.num_vertices):
            if v != u:
                tempdistances=distances[v]
                
                # Considera apenas vértices alcançáveis
                if tempdistances != float('inf'):
                    sum_distances += tempdistances
                    reachable_vertices += 1

        if sum_distances == 0.0 or reachable_vertices == 0:
            return 0.0
        
        # Normaliza pela quantidade de vértices alcançáveis
        return reachable_vertices / sum_distances
    
    def get_betweenness_centrality(self, normalize=True):
        """
        Calcula a Centralidade de Intermediação (Betweenness Centrality) para todos os nós
        usando o Algoritmo de Brandes (baseado no Dijkstra).
        
        Retorna: Um dicionário {node: betweenness_score}.
        """
        num_nodes = self.num_vertices
        # Inicializa o score de intermediação de todos os nós com 0.0
        betweenness = {node: 0.0 for node in range(num_nodes)}
    
        # Itera sobre cada nó 's' como a origem (source)
        for s in range(num_nodes):
        # Roda Dijkstra a partir de 's'.
        # O terceiro retorno (shortest_path_count) é crucial aqui.
            distances, predecessors, shortest_path_count = self.dijkstra(s)
        
            # Pilha (Stack): Armazena os nós na ordem decrescente de distância de 's'
            stack = []
            # Dependência (delta): Usada para calcular o quanto um nó depende de seus predecessores
            dependency = {node: 0.0 for node in range(num_nodes)}
            
            # Preenche a pilha com os nós alcançáveis
            # Filtra os nós pela distância finita
            sorted_nodes = [node for node in range(num_nodes) if distances[node] != float('inf')]
            
            # Ordena os nós por distância para processar de trás para frente (folhas -> raiz)
            sorted_nodes.sort(key=lambda node: distances[node], reverse=True)
            
            for v in sorted_nodes:
                if v != s:
                    stack.append(v)
            
            # 2. Fase de Acumulação
            while stack:
                w = stack.pop()

                # Para cada predecessor 'v' de 'w' no caminho mais curto
                for v in predecessors[w]:
                    
                    # Proporção de caminhos mais curtos de s->w que passam por v
                    if shortest_path_count[w] > 0 and shortest_path_count[v] > 0:
                        fraction = shortest_path_count[v] / shortest_path_count[w]
                    else:
                        fraction = 0.0  
                    # Acumula a dependência: delta_w = (shortest_path_count[v] / shortest_path_count[w]) * (1 + delta_w)
                    dependency[v] += fraction * (1.0 + dependency[w])
                # Adiciona a dependência ao score de Betweenness de 'w'
                # (Exclui a Centralidade de Intermediação do nó de partida 's')
                if w != s:
                    betweenness[w] += dependency[w]
                    
        # 3. Normalização
        if normalize:
            N = num_nodes
            
            # Fator de normalização para grafos dirigidos: (N-1) * (N-2)
            # O fator para grafos dirigidos é: (N-1) * (N-2)
            # Se for não-dirigido, seria: (N-1) * (N-2) / 2
            
            # Fator máximo (Max possible score)
            max_score = (N - 1) * (N - 2) 

            if max_score > 0:
                for node in betweenness:
                    # Divide pelo score máximo para obter um valor entre 0 e 1
                    betweenness[node] = betweenness[node] / max_score
        return betweenness        

    def eigenvector_centrality(self, max_iterations=100, tolerance=1.0e-6):
        """
        Calcula a centralidade do autovetor para todos os nós usando o método de potência.
        Retorna: Um dicionário {node: eigenvector_score}.
        """
        num_nodes = self.num_vertices
        if num_nodes == 0:
            return {}
        
        # Inicializa o vetor de centralidade com valores iguais
        centrality = {node: 1.0 / num_nodes for node in range(num_nodes)}

        #2 iterações do método de potência
        for _ in range(max_iterations):
            new_scores = {node: 0.0 for node in range(num_nodes)}
            norm_sum_sq = 0.0 # Soma dos quadrados para normalização

            for u in range(num_nodes):
                score_u = 0.0 # Score temporário para o nó u
                
                for v in range(num_nodes):
                    if v in self.adj_list and u in self.adj_list[v]:
                        weight = self.adj_list[v][u]
                        score_u += weight * centrality[v]
                
                new_scores[u] = score_u
                norm_sum_sq += score_u * score_u

            # Normaliza os novos scores
            norm = math.sqrt(norm_sum_sq)
            if norm > 0:
                #verifica convergência
                diff_sq=0.0
                for node in range(num_nodes):
                    new_scores[node] /= norm
                    # Calcula a diferença ao quadrado para verificação de convergência
                    diff_sq += (new_scores[node] - centrality[node]) ** 2
            
            # Verifica se convergiu ao critério de tolerância
            if math.sqrt(diff_sq) < tolerance:
                return new_scores
            
            # Atualiza os scores para a próxima iteração
            centrality = new_scores
        else:
            return new_scores #caso em que todos os scores são zeros

        return  centrality     


    # --- Metricas de estrutura ---
    def get_network_density(self):
        """
        Calcula a densidade do grafo
        """
        N=self.num_vertices
        max_edges=N*(N-1)
        if max_edges==0:
            return 0.0
        existing_edges=self.get_edge_count()

        return existing_edges / max_edges
    
    def get_clustering_coefficient(self, u):
        """
        Calcula o coeficiente de aglomeração do vértice u
        """
        self.validate_index(u)
        neighbors = list(self.adj_list[u].keys())
        k = len(neighbors)

        if k < 2:
            return 0.0
        
        #maximo de conexões possíveis entre os vizinhos
        possible_connections = k * (k - 1) / 2
        # Conta conexões entre os vizinhos
        connections = 0
        #conta todas as conexões entre os vizinhos

        for v in neighbors:
            for w in neighbors:
                if v != w and self.has_edge(v, w): #verifica se existe conexão entre os vizinhos
                    connections += 1
        if possible_connections == 0:
            return 0.0
        return connections / possible_connections
    
    def get_assortativity_coefficient(self):
        """
        Calcula o coeficiente de Assortatividade (Correlação de Grau Out-In).
        Mede a correlação entre o grau de saída (out-degree) de um nó de origem (u) 
        e o grau de entrada (in-degree) de seu vizinho de destino (v).        
        Retorna um valor entre -1 e 1.
        """
        # Calcula as médias necessárias
        m = self.get_edge_count()
        if m == 0:
            return 0.0
        
        #armazena os graus de saída e entrada
        out_degrees = {u:self.get_vertex_out_degree(u) for u in range(self.num_vertices)}
        in_degrees = {v:self.get_vertex_in_degree(v) for v in range(self.num_vertices)}

        # variáveis para a formula de correlação de Pearson
        sum_x = 0.0
        sum_y = 0.0
        sum_x2 = 0.0
        sum_y2 = 0.0
        sum_xy = 0.0

        #itera sobre todas as arestas para calcular os somatórios
        for u in range(self.num_vertices):
            for v in self.adj_list[u].keys():
                x= out_degrees[u] # grau de saída de u
                y= in_degrees[v]  # grau de entrada de v

                sum_x += x
                sum_y += y
                sum_x2 += x * x
                sum_y2 += y * y
                sum_xy += x * y

        # Calcula a correlação de Pearson
        numerator = m * sum_xy - sum_x * sum_y
        denominator = math.sqrt((m * sum_x2 - sum_x * sum_x) * (m * sum_y2 - sum_y * sum_y))
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    # --- Metricas de comunidade ---
    def get_edge_betweenness_centrality(self):
        """
        Calcula a Centralidade de Intermediação de Aresta (Edge Betweenness Centrality) 
        usando uma adaptação do Algoritmo de Brandes (Dijkstra).
    
        Retorna: Um dicionário de scores {(u, v): score}.
        """
        num_nodes = self.num_vertices
        # Inicializa o score de intermediação de aresta para todas as arestas existentes
        edge_betweenness = {}
        for u in range(num_nodes):
            for v in self.adj_list[u].keys():
                edge_betweenness[(u, v)] = 0.0

        # Itera sobre cada nó 's' como a origem (source)
        for s in range(num_nodes):
            # O Dijkstra já retorna: distâncias, predecessores, e contagem de caminhos mais curtos
            distances, predecessors, shortest_path_count = self.dijkstra(s)
            
            stack = []
            dependency = {node: 0.0 for node in range(num_nodes)}
            
            # Ordena os nós por distância decrescente para processar de trás para frente
            sorted_nodes = [node for node in range(num_nodes) if distances[node] != float('inf')]
            sorted_nodes.sort(key=lambda node: distances[node], reverse=True)
            
            for v in sorted_nodes:
                if v != s:
                    stack.append(v)
            
            # Fase de Acumulação para Arestas
            while stack:
                w = stack.pop()
                
                # Itera sobre os predecessores 'v' de 'w' no caminho mais curto
                for v in predecessors[w]:
                    
                    # Proporção de caminhos mais curtos de s->w que passam por v
                    if shortest_path_count[w] > 0 and shortest_path_count[w] > 0:
                        fraction = shortest_path_count[v] / shortest_path_count[w]
                    else:
                        fraction = 0.0
                        
                    # A contribuição de Betweenness da aresta (v -> w)
                    edge_contrib = fraction * (1.0 + dependency[w])
                    
                    # Adiciona a contribuição ao score da aresta (v, w)
                    edge_betweenness[(v, w)] += edge_contrib
                    
                    # Acumula a dependência para o nó 'v'
                    dependency[v] += edge_contrib

        return edge_betweenness
    
    def get_bridge_ties(self, top_n=10): #top_n é o número de pontes a retornar, ou seja, o top 10 mais significativas
        """
        Identifica todas as pontes (bridges) no grafo.
        Uma ponte é uma aresta que, se removida, aumenta o número de componentes conectados do grafo.
        
        Retorna: Uma lista de tuplas representando as pontes [(u1, v1), (u2, v2), ...].
        """
        edge_betweenness = self.get_edge_betweenness_centrality()
    
        # Ordena as arestas pelo score em ordem decrescente
        # item[1] é o score
        sorted_edges = sorted(edge_betweenness.items(), key=lambda item: item[1], reverse=True)
        
        bridging_ties_list = []
        
            
        for (u, v), score in sorted_edges[:top_n]:
            # Converte IDs (inteiros) para rótulos de usuário (strings)
            u_label = self.get_label(u)
            v_label = self.get_label(v)
            # Ignora pontuações zero
            if score > 0:
                bridging_ties_list.append((u_label, v_label, score))


        return bridging_ties_list
    
    def get_connected_components(self):
        """
        Usa Busca em Largura para encontrar os Componentes Conexos do grafo.
        esta é uma forma para identificar grupos de usuários que podem se alcançar mutualmente.
        Retorna: Uma lista de comunidades (cada uma é uma lista de rótulos de usuário).
        """
        num_nodes = self.num_vertices
        visited = [False] * num_nodes
        communities = []
        
        def bfs(start_node):
            queue = [start_node]
            component_ids = set()
            visited[start_node] = True
            
            while queue:
                u = queue.pop(0)
                component_ids.add(u)
                
                # Itera sobre todos os nós para encontrar vizinhos de entrada E saída de 'u'
                for v in range(num_nodes):
                    
                    is_neighbor = False
                    # 1. Vizinhos de Saída: u -> v
                    if v in self.adj_list[u]:
                        is_neighbor = True
                    # 2. Vizinhos de Entrada: v -> u
                    elif u in self.adj_list[v]:
                        is_neighbor = True
                    
                    if is_neighbor and not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        
            return component_ids

        for i in range(num_nodes):
            if not visited[i]:
                component_ids = bfs(i)
                if component_ids:
                    # Converte os IDs de volta para rótulos (nomes de usuário)
                    community_labels = [self.get_label(node_id) for node_id in component_ids]
                    communities.append(community_labels)
                    
        return communities
    
        
        

        
    
    

    
