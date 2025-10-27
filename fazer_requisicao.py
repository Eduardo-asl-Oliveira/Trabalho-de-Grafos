#importa a biblioteca
import requests 
import json
import os                 
from dotenv import load_dotenv 



#--- Le o token ------
load_dotenv() # Isso carrega as variáveis do arquivo .env para o ambient

#le o token do .env la
MEU_TOKEN = os.environ.get("GITHUB_TOKEN")

if not MEU_TOKEN:
    raise ValueError("Erro: Token do GitHub não encontrado. Verifique seu arquivo .env")


#--- Repositorio escolhido----
user = "tiangolo"
repo_name = "fastapi"

#---cabecalho de autentificacao nas requisicoes---
headers = {
    "Authorization": f"Bearer {MEU_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


# --- Listas para guardar os dados ---
issues_fechadas = []
issues_coments = []
pull_coments = []
prs_aberto = []
prs_mergeados = []
todas_revisoes = []


#---------------------------------------------------------------------
# BUSCANDO FECHAMENTO DE ISSUES
url_issues_fechadas = f"https://api.github.com/repos/{user}/{repo_name}/issues?state=closed&per_page=5"
print(f"buscando issues fechadas para: {url_issues_fechadas}")

try:
    response_issues = requests.get(url_issues_fechadas, headers=headers)
    
    
    if response_issues.status_code == 200:
        issues_fechadas = response_issues.json()
        print(f"  -> Sucesso! {len(issues_fechadas)} issues encontradas.")
    else:
        print(f"erro ao encontrar issues: {response_issues.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")


#---------------------------------------------------------------------
# BUSCANDO COMENTÁRIOS EM ISSUES
url_issue_coments = f"https://api.github.com/repos/{user}/{repo_name}/issues/comments?per_page=5"
print(f"\nbuscando comentarios em issues para: {url_issue_coments}")

try:
    response_issue_coments = requests.get(url_issue_coments, headers=headers)
    
    if response_issue_coments.status_code == 200:
    
        issues_coments = response_issue_coments.json()
        print(f"  -> Sucesso! {len(issues_coments)} comentários encontrados.")
    else:
        print(f"erro ao encontrar comentarios: {response_issue_coments.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")


#---------------------------------------------------------------------
# BUSCANDO COMENTARIOS EM PULL REQUEST (No código)
url_pull_comments = f"https://api.github.com/repos/{user}/{repo_name}/pulls/comments?per_page=5"
print(f"\nbuscando comentarios em pull request para: {url_pull_comments}")

try:
    response_pull_coments = requests.get(url_pull_comments, headers=headers)
    
    if response_pull_coments.status_code == 200:
        pull_coments = response_pull_coments.json()
        print(f"  -> Sucesso! {len(pull_coments)} comentários de código encontrados.")
    else:
        print(f"erro ao encontrar comentarios em pull requests: {response_pull_coments.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")


#---------------------------------------------------------------------
# BUSCANDO ABERTURA DE PULL REQUEST
url_prs_abertos = f"https://api.github.com/repos/{user}/{repo_name}/pulls?state=open&sort=created&direction=desc&per_page=5"
print(f"\nbuscando PRs abertos para: {url_prs_abertos}")

try:
    response_prs_abertos = requests.get(url_prs_abertos, headers=headers)
    
    if response_prs_abertos.status_code == 200:
        prs_aberto = response_prs_abertos.json()
        print(f"  -> Sucesso! {len(prs_aberto)} PRs abertos encontrados.")
    else:
        print(f"erro ao encontrar abertura de pull requests: {response_prs_abertos.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")


#---------------------------------------------------------------------
# BUSCANDO MERGE DE PULL REQUEST
url_prs_fechados = f"https://api.github.com/repos/{user}/{repo_name}/pulls?state=closed&sort=updated&direction=desc&per_page=10"
print(f"\nbuscando os PRs fechados para achar os 'mergeados': {url_prs_fechados}")

try:
    response_prs_fechados = requests.get(url_prs_fechados, headers=headers)

    if response_prs_fechados.status_code == 200:
        prs_fechados = response_prs_fechados.json()

        # Filtramos a lista para pegar só os que foram 'merged'
        prs_mergeados = [pr for pr in prs_fechados if pr['merged_at'] is not None]
        print(f"  -> Sucesso! {len(prs_mergeados)} PRs 'mergeados' encontrados.")
    else:
        print(f"erro ao encontrar PRs fechados: {response_prs_fechados.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")


#---------------------------------------------------------------------
# BUSCANDO REVISAO E APROVACAO DE PULL REQUEST
# Vamos usar a lista 'prs_aberto' que pegamos acima como exemplo
# Este é o "loop N+1" que discutimos.

print(f"\nBuscando revisões para os {len(prs_aberto)} PRs abertos...")

# Loop para cada PR que encontramos na lista 'prs_aberto'
for pr in prs_aberto:
    pr_number = pr['number']
    print(f"  ...Buscando revisões para o PR #{pr_number}...")
    
    # Cria a URL específica para as REVISÕES daquele PR
    url_revisoes = f"https://api.github.com/repos/{user}/{repo_name}/pulls/{pr_number}/reviews"
    
    try:
        # Faz a chamada autenticada
        response_revisoes = requests.get(url_revisoes, headers=headers)
        
        if response_revisoes.status_code == 200:
            revisoes_deste_pr = response_revisoes.json()
            if revisoes_deste_pr:
                print(f"    -> Encontradas {len(revisoes_deste_pr)} revisões.")
                # Adiciona as revisões encontradas na nossa lista principal
                todas_revisoes.extend(revisoes_deste_pr)
            else:
                print(f"    -> Nenhuma revisão encontrada para este PR.")
        else:
            print(f"    -> Erro ao buscar revisões para o PR #{pr_number}: {response_revisoes.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao buscar revisões: {e}")

print("\n--- COLETA DE DADOS FINALIZADA ---")
print(f"Total de PRs abertos coletados: {len(prs_aberto)}")
print(f"Total de PRs mergeados coletados: {len(prs_mergeados)}")
print(f"Total de revisões (Aprovações) coletadas: {len(todas_revisoes)}")
