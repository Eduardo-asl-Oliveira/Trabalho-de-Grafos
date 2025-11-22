from src.AbstractGraph import AbstractGraph 

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