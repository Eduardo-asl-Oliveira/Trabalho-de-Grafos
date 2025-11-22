from abc import ABC, abstractmethod

class AbstractGraph(ABC):
    """
    Classe base abstrata. Define o contrato e atributos comuns.
    """
    
    def __init__(self, num_vertices):
        # Este é o construtor que estava faltando!
        self.num_vertices = num_vertices
        self.vertex_weights = [0.0] * num_vertices
        self.labels = [None] * num_vertices  
        self.label_to_id = {}               
        self.count_vertices_used = 0

    # --- Auxiliares para Mapeamento (String <-> Int) ---
    def add_vertex_label(self, label):
        """Associa um nome (ex: 'dracula') a um ID numérico."""
        if label not in self.label_to_id:
            if self.count_vertices_used >= self.num_vertices:
                 # Se tentar adicionar mais do que o planejado
                 raise ValueError(f"Capacidade do grafo excedida ({self.num_vertices}).")
            
            idx = self.count_vertices_used
            self.label_to_id[label] = idx
            self.labels[idx] = label
            self.count_vertices_used += 1
            return idx
        return self.label_to_id[label]

    def get_label(self, v):
        if 0 <= v < len(self.labels):
            return self.labels[v]
        return None

    def validate_index(self, idx):
        if idx < 0 or idx >= self.num_vertices:
            raise ValueError(f"Índice de vértice inválido: {idx}")

    # --- Métodos Concretos Comuns ---
    def get_vertex_count(self):
        return self.num_vertices

    def set_vertex_weight(self, v, w):
        self.validate_index(v)
        self.vertex_weights[v] = w

    def get_vertex_weight(self, v):
        self.validate_index(v)
        return self.vertex_weights[v]
        
    # --- Exportação para GEPHI ---
    def export_to_gephi(self, path):
        # Gera XML simples para abrir no Gephi
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">')
        xml.append('  <graph mode="static" defaultedgetype="directed">')
        xml.append('    <nodes>')
        for i in range(self.num_vertices):
            lbl = self.labels[i] if self.labels[i] else str(i)
            xml.append(f'      <node id="{i}" label="{lbl}" />')
        xml.append('    </nodes>')
        xml.append('    <edges>')
        eid = 0
        for u in range(self.num_vertices):
            for v in range(self.num_vertices):
                if self.has_edge(u, v):
                    w = self.get_edge_weight(u, v)
                    xml.append(f'      <edge id="{eid}" source="{u}" target="{v}" weight="{w}" />')
                    eid += 1
        xml.append('    </edges>')
        xml.append('  </graph>')
        xml.append('</gexf>')
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(xml))
        print(f"Exportado para {path}")

    # --- Métodos Abstratos (Obrigatórios para as filhas) ---
    @abstractmethod
    def has_edge(self, u, v): pass
    
    @abstractmethod
    def add_edge(self, u, v): pass
    
    @abstractmethod
    def remove_edge(self, u, v): pass
    
    @abstractmethod
    def get_edge_weight(self, u, v): pass
    
    @abstractmethod
    def set_edge_weight(self, u, v, w): pass
    
    @abstractmethod
    def get_edge_count(self): pass
    
    @abstractmethod
    def is_successor(self, u, v): pass
    
    @abstractmethod
    def is_predecessor(self, u, v): pass
    
    @abstractmethod
    def is_divergent(self, u1, v1, u2, v2): pass
    
    @abstractmethod
    def is_convergent(self, u1, v1, u2, v2): pass
    
    @abstractmethod
    def is_incident(self, u, v, x): pass
    
    @abstractmethod
    def get_vertex_in_degree(self, u): pass
    
    @abstractmethod
    def get_vertex_out_degree(self, u): pass
    
    @abstractmethod
    def is_connected(self): pass