Análise de Interações em Repositórios GitHub via Teoria dos Grafos
Este projeto consiste no desenvolvimento de uma ferramenta computacional para modelagem, processamento e análise de dados de um repositório de código aberto do GitHub. O objetivo é aplicar conceitos de Teoria dos Grafos e métricas de Redes Complexas para entender as dinâmicas de colaboração entre usuários.

Trabalho prático da disciplina Teoria de Grafos e Computabilidade (2025/2) do curso de Engenharia de Software da PUC Minas.

🎯 Objetivo
Analisar as interações dos colaboradores de um repositório real (com mais de 5.000 estrelas ), identificando padrões de colaboração, influenciadores e grupos de trabalho através da construção e análise de grafos.

📂 Repositório Analisado
Nome: [tema do drácula]

URL: [https://github.com/dracula/dracula-theme]

Linguagem Principal: [Python]

📐 Modelagem do Grafo

O sistema modela os dados extraídos do GitHub da seguinte forma:

Vértices (Nós): Usuários do GitHub.

Arestas (Relações): Interações entre usuários.

Tipo de Grafo: Simples e direcionado (relações bidirecionais usam arestas antiparalelas).

Pesos das Interações (Grafo Integrado)
Para o grafo consolidado, as arestas possuem pesos baseados na intensidade da colaboração técnica:
| Tipo de Interação | Peso |  Descrição |
| ----------------- | ---- | ---------- |
| Comentário em Issue/PR | 2 | Interação leve | 
| Abertura de Issue (comentada por outro) | 3 | Interação média |  
| Revisão/Aprovação de Pull Request | 4 | Colaboração técnica forte |
| Merge de Pull Request | 5 | Colaboração técnica máxima | 

Além do grafo integrado, o sistema também processa grafos isolados para cada tipo de relação.


🏗️ Arquitetura e Implementação

A ferramenta foi desenvolvida seguindo a estrutura de classes obrigatória:

Classes Principais

AbstractGraph: Classe abstrata que define a API comum e atributos compartilhados.

AdjacencyMatrixGraph: Implementação concreta utilizando Matriz de Adjacência.

AdjacencyListGraph: Implementação concreta utilizando Listas de Adjacência.

Funcionalidades da API (Métodos Obrigatórios)
A implementação suporta as seguintes operações :

Manipulação básica: addEdge, removeEdge, hasEdge.

Informações de grau: getVertexInDegree, getVertexOutDegree.

Relações: isSucessor, isPredessor, isIncident.

Análise estrutural: isConnected, isCompleteGraph, isDivergent, isConvergent.

Gestão de pesos: setVertexWeight, getEdgeWeight, etc.


Exportação: Método exportToGEPHI para visualização externa.

📊 Análise de Dados e Métricas
Na "Etapa 3", a ferramenta aplica algoritmos para extrair as seguintes métricas do repositório:

1. Métricas de Centralidade 

Degree Centrality: Participação ativa em revisões e discussões.

Betweenness Centrality: Identificação de usuários "ponte" entre grupos.

Closeness Centrality: Velocidade de acesso à informação na rede.

PageRank / Eigenvector: Influência ponderada do colaborador.

2. Estrutura e Coesão 

Densidade da Rede: Quão colaborativo é o projeto como um todo.

Coeficiente de Aglomeração (Clustering): Tendência de formação de "panelinhas".

Assortatividade: Se "hubs" se conectam com outros "hubs" ou com iniciantes.

3. Comunidades 

Detecção de Comunidades (Modularidade): Identificação de times informais.

Bridging Ties: Análise de conexões entre diferentes comunidades.

🚀 Como Executar
Pré-requisitos
[Python] 
Acesso à Internet (para mineração de dados do GitHub)

Instalação
Clone o repositório:

git clone [https://github.com/Eduardo-asl-Oliveira/Trabalho-de-Grafos.git]

👥 Autores

[Eduardo Alves Salgado Lisboa Oliveira]

[Gabriel Batista de Almeida]

[Gabriel El-dine Breguez da Cunha]

Projeto desenvolvido para a disciplina de Teoria de Grafos e Computabilidade - PUC Minas.
