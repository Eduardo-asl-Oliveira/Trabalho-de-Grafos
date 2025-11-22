from src.AbstractGraph import AbstractGraph

class AdjacencyMatrixGraph(AbstractGraph):
    """
    Implementação utilizando Matriz de Adjacência.
    """

    def __init__(self, num_vertices): # [cite: 49]
        super().__init__(num_vertices)
        # Inicializa matriz N x N com None ou 0
        # Usamos 0.0 para indicar ausência de aresta para facilitar lógica de pesos
        self.matrix = [[0.0] * num_vertices for _ in range(num_vertices)]
        self.num_edges = 0

    def get_edge_count(self):
        return self.num_edges

    def has_edge(self, u, v):
        self.validate_index(u)
        self.validate_index(v)
        return self.matrix[u][v] != 0.0

    def add_edge(self, u, v):
        self.validate_index(u)
        self.validate_index(v)
        
        # Idempotente e sem laços [cite: 73, 74]
        if u == v:
            return # Não permite laços
            
        if not self.has_edge(u, v):
            self.matrix[u][v] = 1.0 # Peso padrão inicial
            self.num_edges += 1

    def remove_edge(self, u, v):
        if self.has_edge(u, v):
            self.matrix[u][v] = 0.0
            self.num_edges -= 1

    def set_edge_weight(self, u, v, w):
        if self.has_edge(u, v):
            self.matrix[u][v] = float(w)

    def get_edge_weight(self, u, v):
        if self.has_edge(u, v):
            return self.matrix[u][v]
        return 0.0

    # --- Lógica de Grafos ---

    def is_successor(self, u, v):
        return self.has_edge(u, v)

    def is_predecessor(self, u, v):
        # Verifica se existe aresta V -> U (V é predecessor de U)
        return self.has_edge(v, u)

    def is_divergent(self, u1, v1, u2, v2):
        # Verifica se as arestas (u1,v1) e (u2,v2) divergem da mesma origem
        if not (self.has_edge(u1, v1) and self.has_edge(u2, v2)):
            raise ValueError("Uma das arestas não existe.")
        return u1 == u2 and v1 != v2

    def is_convergent(self, u1, v1, u2, v2):
        # Verifica se as arestas convergem para o mesmo destino
        if not (self.has_edge(u1, v1) and self.has_edge(u2, v2)):
            raise ValueError("Uma das arestas não existe.")
        return v1 == v2 and u1 != u2

    def is_incident(self, u, v, x):
        # Verifica se x é uma das pontas da aresta (u, v)
        if not self.has_edge(u, v):
            return False
        return x == u or x == v

    def get_vertex_in_degree(self, u):
        self.validate_index(u)
        degree = 0
        for i in range(self.num_vertices):
            if self.matrix[i][u] != 0.0:
                degree += 1
        return degree

    def get_vertex_out_degree(self, u):
        self.validate_index(u)
        degree = 0
        for j in range(self.num_vertices):
            if self.matrix[u][j] != 0.0:
                degree += 1
        return degree

    def is_empty_graph(self):
        return self.num_edges == 0

    def is_complete_graph(self):
        # Grafo completo simples direcionado: n*(n-1) arestas
        max_edges = self.num_vertices * (self.num_vertices - 1)
        return self.num_edges == max_edges

    def is_connected(self):
        # Verifica conectividade no sentido fraco (ignorando direção) usando BFS
        # Para verificar se "o grafo é conectado"
        if self.num_vertices == 0: return True
        
        visited = [False] * self.num_vertices
        queue = [0] # Começa do vértice 0
        visited[0] = True
        count_visited = 0
        
        while queue:
            u = queue.pop(0)
            count_visited += 1
            
            for v in range(self.num_vertices):
                # Verifica aresta em QUALQUER direção (u->v ou v->u) para conectividade fraca
                if (self.matrix[u][v] != 0.0 or self.matrix[v][u] != 0.0):
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        
        return count_visited == self.num_vertices