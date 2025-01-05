#%% Parte 1: Importando as bibliotecas necessárias
import json
from pathlib import Path
from phi.assistant.duckdb import DuckDbAssistant
from dotenv import load_dotenv
from apify_client import ApifyClient
import os

#%% Parte 2: Configuração inicial
load_dotenv()

# Definindo o caminho para salvar os dados
caminho_arquivo = Path("dados_mercadolivre.json")

# Obtendo o token da API do Apify
token_apify = os.getenv("APIFY_TOKEN")
if not token_apify:
    print("Erro: Token do Apify não encontrado!")
    print("Crie um arquivo .env com seu token do Apify")
    exit()

#%% Parte 3: Configurando a busca no Mercado Livre
cliente = ApifyClient(token_apify)

# Pergunta para usuário se quer usar dados já coletados ou buscar novos
input_usar_dados_ja_coletados = input("Você quer usar dados já coletados? (s/N): ")

if input_usar_dados_ja_coletados.lower() == "s":
    pass
else:
    # Definindo o que queremos buscar no Mercado Livre
    input_busca = input("Digite o que você quer buscar no Mercado Livre: ")
    input_paginas = int(input("Digite o número de páginas que você quer buscar (cada página tem ~50 produtos): "))

    configuracao_busca = {
        "keyword": input_busca,
        "pages": input_paginas,
        "promoted": False,
        "country": "BR"  # Definindo Brasil como país de busca
    }

    #%% Parte 4: Buscando os dados
    print("Buscando dados do Mercado Livre...")

    # Iniciando a busca com o Apify (usando o actor do Mercado Livre)
    execucao = cliente.actor("PataeAthih1fU9TX7").call(run_input=configuracao_busca)

    # Coletando os resultados
    dados_produtos = list(cliente.dataset(execucao["defaultDatasetId"]).iterate_items())

    print(f"Encontrados {len(dados_produtos)} produtos!")

    #%% Parte 5: Preparando os dados para análise
    print("\nPreparando os dados...")

    # Criando uma lista para guardar os dados normalizados
    dados_normalizados = []

    # Normalizando cada produto
    for produto in dados_produtos:
        produto_normalizado = {
            'titulo': produto.get('eTituloProduto', ''),
            'preco_atual': produto.get('novoPreco', '').replace('.', '').replace(',', '.'),
            'preco_anterior': produto.get('precoAnterior', '').replace('.', '').replace(',', '.'),
            'imagem_url': produto.get('imagemLink', ''),
            'marca': produto.get('produtoMarca', ''),
            'link': produto.get('zProdutoLink', '')
        }
        dados_normalizados.append(produto_normalizado)

    #%% Parte 6: Salvando os dados
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
            "description": "Informações sobre produtos do Mercado Livre",
            "path": str(caminho_arquivo),
        }]
    }),
    markdown=True,
    show_tool_calls=True,
    base_dir=Path("analises")
)

#%% Parte 8: Fazendo algumas análises
print("\nAnalisando os dados...")

# Lista de perguntas para análise
perguntas = [
    "Quais são os campos disponíveis na tabela de produtos?",
    "Qual é a média de preços dos produtos?",
    "Quais são os 5 produtos mais baratos?",
    "Quais são os 5 produtos mais caros?"
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