# 1. primeiro o meu token é lido no arquivo .env para que possa ser realizada a requisicao
# 2. escolho o repositorio e o usuario do repositorio
# 3. a funcao coletar_dados_paginados faz requisicoes pagina por pagina do repositorio escolhido e armazena em dados da pagina
# 4. filtro a os dados e armazeno as issues em uma lista e faco um for para cada item da lista
    # a) para cada issue encontrada acho o autor e quem fechou a issue
    # b) adiciono no grafo 2
    # c) verifico se cada issue tem comentarios, se tiver faco mais uma requisicao
    # d) encontro o dono do comentario 
    # e) adiciono no grafo 1
# 5. filtro a os dados e armazeno as pull request em uma lista e faco um for para cada item da lista
    # a) acho o dono da pull request e o usuario que fez o merge
    # b) adiciono no grafo 3
    # c) se a pr tiver revisoes faco outra requisicao
    # D) faco um for para cada revisao e acho quem fez a review
    # e) adiciono no grafo 3 
    # f) verifico se tem comentarios em pr e se tiver faco mais uma requisicao
    # g) encontro quem fez o comentario 
    # h) add no grafo 1 (quem comentou e quem recebeu)




# --- importa a biblioteca ---
import requests 
import json
import os                 
from dotenv import load_dotenv 
import time

#--- Le o token ------
load_dotenv() # Isso carrega as variáveis do arquivo .env para o ambient

#le o token do .env la
MEU_TOKEN = os.environ.get("GITHUB_TOKEN")

if not MEU_TOKEN:
    raise ValueError("Erro: Token do GitHub não encontrado. Verifique seu arquivo .env")

#--- Repositorio escolhido----
user = "dracula"
repo_name = "dracula-theme"

#---cabecalho de autentificacao nas requisicoes---
headers = {
    "Authorization": f"Bearer {MEU_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# --- Grafos ---
grafo_1_comentarios = {}
grafo_2_fechamento_issue = {}
grafo_3_revisoes_e_merges = {}
grafo_integrado_ponderado = {} 



#-----------------------------------------------------------------------
# --- RECEBE A REQUISICAO E ARMAZENA ---
#-----------------------------------------------------------------------
def coletar_dados_paginados(url_base):
    """
    Busca todos os dados de um endpoint da API do GitHub,
    lidando automaticamente com a paginação.
    """
    print(f"Iniciando coleta em massa de: {url_base}")
    dados_completos = []
    pagina = 1
    
    while True:
        # Pede a página 'X', com 100 itens por página (o máximo permitido)
        # O state=all garante que pegamos issues abertas E fechadas
        url = f"{url_base}?page={pagina}&per_page=100&state=all"
        print(f"  ...buscando página {pagina}...")
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                dados_da_pagina = response.json()
                
                # Se a página veio vazia, significa que acabaram os dados
                if not dados_da_pagina:
                    print(f"  Coleta finalizada. Total de {len(dados_completos)} itens coletados.")
                    break  # Sai do loop while
                
                # Adiciona os dados da página na nossa lista principal
                dados_completos.extend(dados_da_pagina)
                pagina += 1
                
            elif response.status_code == 403:
                # Se atingiu o limite de requisições
                print("  !!! ATINGIU O LIMITE DE REQUISIÇÕES (403). Aguardando 10 minutos... !!!")
                time.sleep(600) # Aguarda 10 minutos
                # O 'continue' faz o loop tentar a MESMA página novamente
                continue 
            else:
                # Outros erros (404, 500, etc.)
                print(f"  Erro {response.status_code} na página {pagina}. Parando coleta.")
                print(response.json()) # Mostra o erro da API
                break # Sai do loop while

        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}. Aguardando 1 minuto antes de tentar novamente...")
            time.sleep(60) # Espera 1 minuto em caso de falha de rede
            continue # Tenta a mesma página novamente
            
        # Pausa de 1 segundo entre as requisições para não sobrecarregar a API
        time.sleep(1) 
            
    return dados_completos


def adicionar_peso(origem, destino, peso):
    """
    Adiciona um peso a uma aresta no grafo_integrado_ponderado.
    Se a aresta (origem -> destino) já existir, o peso é somado.
    """
    
    # Garante que o usuário de 'origem' exista no grafo
    if origem not in grafo_integrado_ponderado:
        grafo_integrado_ponderado[origem] = {}
        
    # Pega o peso atual (ou 0 se a aresta não existir)
    peso_atual = grafo_integrado_ponderado[origem].get(destino, 0)
    
    # Soma o novo peso e atualiza o grafo
    grafo_integrado_ponderado[origem][destino] = peso_atual + peso
    
    # Imprime a ação para vermos o que está acontecendo
    print(f"    [GRAFO PONDERADO] Aresta: {origem} -> {destino} | Peso adicionado: +{peso} | Peso total: {grafo_integrado_ponderado[origem][destino]}")






#-----------------------------------------------------------------------
# --- COLETA E PROCESSA AS ISSUES ---
#-----------------------------------------------------------------------
print("\n--- INICIANDO COLETA DE ISSUES ---")
url_base_issues = f"https://api.github.com/repos/{user}/{repo_name}/issues"

todas_as_issues = coletar_dados_paginados(url_base_issues)# Chama a função que faz a paginação

# --- Processando as issues ---
print("\n--- INICIANDO PROCESSAMENTO DAS ISSUES ---")

for issue in todas_as_issues:
    
    # 1. Ignora PRs (eles vêm misturados)
    if "pull_request" in issue:
        continue

    # 2. Identifica o NÓ DE DESTINO (Dono)
    # Este é o 'Usuario B' para todas as interações desta issue
    usuario_B_dono = issue['user']['login']

    # --- Lógica para o Grafo 2 (Fechamento) ---
    # Verifica se a issue foi fechada por alguém
    if issue['closed_by']:
        # Identifica o NÓ DE ORIGEM (Quem fechou)
        usuario_A_fechou = issue['closed_by']['login']
        
        # Garante que não foi fechada pelo próprio dono
        if usuario_A_fechou != usuario_B_dono:
            # Adiciona a aresta A -> B no Grafo 2
            print(f"  [Grafo 2] Aresta: {usuario_A_fechou} -> {usuario_B_dono}")
            grafo_2_fechamento_issue.setdefault(usuario_A_fechou, set()).add(usuario_B_dono)

    # --- Lógica para o Grafo 1 (Comentários) ---
    # Verifica se a issue tem comentários
    if issue['comments'] > 0:
        
        # FAZ A "MINI-LEITURA" (Requisição N+1)
        url_comentarios = issue['comments_url']
        try:
            print(f"  Buscando {issue['comments']} comentários para Issue #{issue['number']}...")
            response_coments = requests.get(url_comentarios, headers=headers)
            time.sleep(0.5) # Pausa para a API
            
            if response_coments.status_code == 200:
                lista_de_comentarios = response_coments.json()
                
                # itera cada comentario
                for comment in lista_de_comentarios:
                    # Identifica o NÓ DE ORIGEM (Autor do comentário)
                    if not comment.get('user'): # Segurança: verifica se o usuário não é nulo
                        continue
                        
                    usuario_A_comentou = comment['user']['login']
                    
                    if usuario_A_comentou != usuario_B_dono:
                        # Adiciona a aresta A -> B no Grafo 1
                        print(f"    [Grafo 1] Aresta: {usuario_A_comentou} -> {usuario_B_dono}")
                        grafo_1_comentarios.setdefault(usuario_A_comentou, set()).add(usuario_B_dono)
                        
                        # --- ADICIONANDO PESOS ---
                        
                        # Comentário em issue: peso 2 
                        # Aresta: Quem comentou (A) -> Dono da Issue (B)
                        adicionar_peso(usuario_A_comentou, usuario_B_dono, 2)
                        
                        # Abertura de issue comentada: peso 3 
                        # Aresta: Dono da Issue (B) -> Quem comentou (A)
                        adicionar_peso(usuario_B_dono, usuario_A_comentou, 3)

        except Exception as e:
            print(f"    Erro ao buscar comentários: {e}")

print("--- Processamento de Issues finalizado. ---")



#-----------------------------------------------------------------------
# --- COLETA E PROCESSA AS PULL REQUESTS ---
#-----------------------------------------------------------------------
print("\n--- INICIANDO COLETA DE PULLS ---")
url_base_pulls = f"https://api.github.com/repos/{user}/{repo_name}/pulls"

# Chama a função que faz a paginação
todas_as_pulls = coletar_dados_paginados(url_base_pulls)


# --- Processando as Pulls (Para Grafos 1 e 3) ---
print("\n--- INICIANDO PROCESSAMENTO DE PULL REQUESTS ---")

for pr in todas_as_pulls:

    # 1. Identifica o NÓ DE DESTINO (Dono)
    if not pr.get('user'):
        continue
    usuario_B_dono = pr['user']['login']

    # --- Lógica para o Grafo 3 (Merges) ---
    merged_by_user = pr.get('merged_by') 
    if merged_by_user:
        usuario_A_merger = merged_by_user['login']
        if usuario_A_merger != usuario_B_dono:
            print(f"  [Grafo 3] Aresta (Merge): {usuario_A_merger} -> {usuario_B_dono}")
            grafo_3_revisoes_e_merges.setdefault(usuario_A_merger, set()).add(usuario_B_dono)
            
            # --- ADICIONANDO PESOS ---
            
            # Merge de pull request: peso 5 
            # Aresta: Quem fez o merge (A) -> Dono do PR (B)
            adicionar_peso(usuario_A_merger, usuario_B_dono, 5)

    # --- Lógica para o Grafo 3 (Revisões / Aprovações) ---
    #
    # Primeiro, verificamos se a URL 'reviews_url' existe
    url_revisoes = pr.get('reviews_url')
    
    if url_revisoes: # Só executa se a URL foi encontrada
        try:
            print(f"  Buscando revisões para PR #{pr['number']}...")
            response_revisoes = requests.get(url_revisoes, headers=headers)
            time.sleep(0.5) # Pausa
            
            if response_revisoes.status_code == 200:
                lista_de_revisoes = response_revisoes.json()
                
                for review in lista_de_revisoes:
                    if review.get('user'):
                        usuario_A_revisor = review['user']['login']
                        if usuario_A_revisor != usuario_B_dono:
                            print(f"    [Grafo 3] Aresta (Revisão): {usuario_A_revisor} -> {usuario_B_dono}")
                            grafo_3_revisoes_e_merges.setdefault(usuario_A_revisor, set()).add(usuario_B_dono)

                            # --- ADICIONANDO PESOS ---
                            
                            # Revisão/aprovação de pull request: peso 4 
                            # Aresta: Quem revisou (A) -> Dono do PR (B)
                            adicionar_peso(usuario_A_revisor, usuario_B_dono, 4)
                            
        except Exception as e:
            print(f"    Erro ao buscar revisões: {e}")
    #
    # --- Lógica para o Grafo 1 (Comentários em PRs) ---
    #
    
    # Isso pega o número, ou retorna 0 se a chave 'comments' não existir.
    if pr.get('comments', 0) > 0:
        
        # Verificamos também a URL de comentários
        url_comentarios = pr.get('comments_url')
        
        if url_comentarios: # Só executa se a URL foi encontrada
            try:
                print(f"  Buscando {pr['comments']} comentários de conversa para PR #{pr['number']}...")
                response_coments = requests.get(url_comentarios, headers=headers)
                time.sleep(0.5) # Pausa
                
                if response_coments.status_code == 200:
                    lista_de_comentarios = response_coments.json()
                    for comment in lista_de_comentarios:
                        if comment.get('user'):
                            usuario_A_comentou = comment['user']['login']
                            if usuario_A_comentou != usuario_B_dono:
                                print(f"    [Grafo 1] Aresta (Comentário): {usuario_A_comentou} -> {usuario_B_dono}")
                                grafo_1_comentarios.setdefault(usuario_A_comentou, set()).add(usuario_B_dono)

                                # --- ADICIONANDO PESOS ---
                                
                                # Comentário em pull request: peso 2 
                                # Aresta: Quem comentou (A) -> Dono do PR (B)
                                adicionar_peso(usuario_A_comentou, usuario_B_dono, 2)
                                
            except Exception as e:
                print(f"    Erro ao buscar comentários de conversa: {e}")

print("--- Processamento de Pull Requests finalizado. ---")



from src.AdjacencyListGraph import AdjacencyListGraph

# 1. Identificar todos os usuários únicos para definir tamanho do grafo
usuarios_unicos = set(grafo_integrado_ponderado.keys())
for origem, destinos in grafo_integrado_ponderado.items():
    usuarios_unicos.update(destinos.keys())

num_vertices = len(usuarios_unicos)
print(f"Criando grafo com {num_vertices} vértices...")

# 2. Instanciar o Grafo (pode escolher Matriz ou Lista)
meu_grafo = AdjacencyListGraph(num_vertices)

# 3. Povoar o Grafo (Mapeando String -> Int)
# Primeiro, registramos todos os usuários para gerar os IDs
for usuario in usuarios_unicos:
    meu_grafo.add_vertex_label(usuario)

# Agora, criamos as arestas com os pesos
for user_origem, conexoes in grafo_integrado_ponderado.items():
    u_id = meu_grafo.label_to_id[user_origem]
    
    for user_destino, peso in conexoes.items():
        v_id = meu_grafo.label_to_id[user_destino]
        
        meu_grafo.add_edge(u_id, v_id)
        meu_grafo.set_edge_weight(u_id, v_id, float(peso))

print(f"Grafo populado! Arestas totais: {meu_grafo.get_edge_count()}")

print("Exportando para Gephi...")
meu_grafo.export_to_gephi("data/rede_dracula.gexf") 
print("Arquivo 'rede_dracula.gexf' gerado com sucesso!")