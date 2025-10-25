#importa a biblioteca
import requests 


#URL da api que vamos usar

user = "Eduardo-asl-Oliveira"

url = "https://api.github.com/users/" + user + "/repos/projeto-cadastro-viacep"

print(f"fazendo uma requisicao GET para: {url}")

try:
    #faz a chamada para a API
    response = requests.get(url)

    #se a chamada deu certo
    if response.status_code == 200:

        #pega a resposta em converte em um dicionario json
        dados = response.json()

        #imprime os dados
        print("---RESPOSTAS DA API---")
        print(f"login: {dados['login']}")
        print(f"name: {dados['name']}")
        print(f"location: {dados['location']}")w
        print(f"bio: {dados['bio']}")
        print(f"public repos: {dados['public_repos']}")
        print(f"followers: {dados['followers']}")
        print(f"following: {dados['following']}")
        print("------------------------")

    else:
        #se a API deu erro
        print(f"erro: a API retornou o status {response.status_code}")

except requests.exceptions.RequestException as e:
    # Se tiver um erro de conexão (ex: sem internet)
    print(f"Erro de conexão ao tentar acessar a API: {e}")