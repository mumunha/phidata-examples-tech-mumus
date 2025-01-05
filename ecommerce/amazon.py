#%% Parte 1: Importando as bibliotecas necessárias
# Primeiro, vamos importar todas as bibliotecas que precisamos
import json  # Para trabalhar com dados JSON
from pathlib import Path  # Para lidar com caminhos de arquivos
from phi.assistant.duckdb import DuckDbAssistant  # Para análise de dados
from dotenv import load_dotenv  # Para carregar variáveis de ambiente
from apify_client import ApifyClient  # Para conectar com a API do Apify
import os  # Para acessar variáveis de ambiente

#%% Parte 2: Configuração inicial
# Carregando as variáveis de ambiente do arquivo .env
load_dotenv()

# Definindo o caminho para salvar os dados
caminho_arquivo = Path("dados_amazon.json")

# Obtendo o token da API do Apify
# O token deve estar no arquivo .env como: APIFY_TOKEN=seu_token_aqui
token_apify = os.getenv("APIFY_TOKEN")
if not token_apify:
    print("Erro: Token do Apify não encontrado!")
    print("Crie um arquivo .env com seu token do Apify")
    exit()


#%% Parte 3: Configurando a busca na Amazon
# Criando o cliente do Apify
cliente = ApifyClient(token_apify)

# Pergunta para usuário se quer usar dados já coletados ou buscar novos
input_usar_dados_ja_coletados = input("Você quer usar dados já coletados? (s/N): ")

if input_usar_dados_ja_coletados.lower() == "s":

    pass

else:
    # Definindo o que queremos buscar na Amazon
    # Você pode modificar a URL para buscar outros produtos
    input_busca = input("Digite o que você quer buscar na Amazon: ")
    input_quantidade = int(input("Digite a quantidade de produtos que você quer buscar: "))

    

    configuracao_busca = {
        "categoryUrls": [
            {"url": f"https://www.amazon.com/s?k={input_busca}"}  # Buscando teclados gamer
        ],
        "maxItemsPerStartUrl": input_quantidade,  
        "useCaptchaSolver": False,
        "scrapeProductVariantPrices": False,
        "scrapeProductDetails": True,
    }

    #%% Parte 4: Buscando os dados
    print("Buscando dados da Amazon...")

    # Iniciando a busca com o Apify
    execucao = cliente.actor("XVDTQc4a7MDTqSTMJ").call(run_input=configuracao_busca)

    # Coletando os resultados
    dados_produtos = list(cliente.dataset(execucao["defaultDatasetId"]).iterate_items())

    print(f"Encontrados {len(dados_produtos)} produtos!")

    #%% Parte 5: Preparando os dados para análise
    print("\nPreparando os dados...")

    # Criando uma lista para guardar os dados normalizados
    dados_normalizados = []

    # Campos que precisam ser convertidos para texto
    campos_especiais = ['attributes', 'productOverview', 'variantDetails', 'aPlusContent']

    # Normalizando cada produto
    for produto in dados_produtos:
        # Convertendo campos especiais para texto
        for campo in campos_especiais:
            if campo in produto:
                produto[campo] = json.dumps(produto[campo])
        dados_normalizados.append(produto)

    #%% Parte 6: Salvando os dados
       

    # Salvando os dados normalizados
    with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados_normalizados, arquivo, indent=2, ensure_ascii=False)

    print(f"Dados salvos em {caminho_arquivo}")

    #%% Parte 7: Configurando o assistente de análise
    print("\nConfigurando o assistente de análise...")

# Criando o assistente DuckDB
assistente = DuckDbAssistant(
    semantic_model=json.dumps({
        "tables": [{
            "name": "produtos",
            "description": "Informações sobre produtos da Amazon",
            "path": str(caminho_arquivo),
        }]
    }),
    markdown=True,
    show_tool_calls=True,
    base_dir=Path("analises")  # Pasta para guardar as análises
)

#%% Parte 8: Fazendo algumas análises
print("\nAnalisando os dados...")

# Lista de perguntas para análise
perguntas = [
    "Quais são os campos disponíveis na tabela de produtos?",
    "Qual é a média de preços dos produtos?",
    "Quais são os 5 produtos mais bem avaliados?"
]

# Analisando cada pergunta
for pergunta in perguntas:
    print(f"\nPergunta: {pergunta}")
    print("-" * 50)
    assistente.print_response(pergunta)

#%% Parte 9: Iniciando o modo interativo
print("\nIniciando modo interativo...")
print("Você pode fazer suas próprias perguntas sobre os dados!")
print("Digite 'exit' para sair")

# Iniciando o modo interativo
assistente.cli_app(markdown=True)